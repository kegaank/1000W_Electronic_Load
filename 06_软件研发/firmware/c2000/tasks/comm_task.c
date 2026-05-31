/**
 * @file    comm_task.c
 * @brief   UART communication task with ESP32.
 *
 * Handles:
 *   - Reading raw bytes from UART RX buffer
 *   - Frame synchronization and CRC validation
 *   - Command dispatch to appropriate handler
 *   - Sending response frames back to ESP32
 *
 * The task polls the UART at 10 ms intervals and processes complete
 * frames. This is not a streaming protocol — each frame is a complete
 * command that gets a complete response.
 *
 * Protocol (binary frame):
 *   [0xAA][0x55][len][cmd][payload...][crc16_lo][crc16_hi]
 *
 * ESP32 is the bus master — it initiates all transactions.
 * C2000 responds within 1 ms of receiving a complete frame.
 */

#include "FreeRTOSConfig.h"
#include "uart.h"
#include "protocol.h"
#include "modes.h"
#include "el1000_types.h"
#include <string.h>

/* ─── RX frame buffer ──────────────────────────────────────────────── */
static uint8_t g_frame_buf[PROTO_FRAME_MAX];
static uint32_t g_frame_pos = 0;
static enum { SYNC0_WAIT, SYNC1_WAIT, LEN_WAIT, PAYLOAD_WAIT, CRC_WAIT } g_rx_state = SYNC0_WAIT;
static uint8_t  g_expected_len = 0;
static uint32_t g_payload_collected = 0;

/* ─── Forward declarations ─────────────────────────────────────────── */
extern void protection_comms_ping(void);

/* ─── Command handler prototypes ──────────────────────────────────── */
static void handle_ping(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len);
static void handle_get_status(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len);
static void handle_get_telemetry(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len);
static void handle_set_mode(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len);
static void handle_set_setpoint(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len);
static void handle_set_output(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len);

/* ─── Command dispatch table ───────────────────────────────────────── */
typedef void (*cmd_handler_t)(const proto_frame_t*, uint8_t*, uint32_t*);
static const cmd_handler_t g_cmd_handlers[256] = {
    [CMD_PING]          = handle_ping,
    [CMD_GET_STATUS]    = handle_get_status,
    [CMD_GET_TELEMETRY] = handle_get_telemetry,
    [CMD_SET_MODE]      = handle_set_mode,
    [CMD_SET_SETPOINT]  = handle_set_setpoint,
    [CMD_SET_OUTPUT]    = handle_set_output,
};

/**
 * @brief  Communication task.
 *
 * @param  pvParameters  Unused.
 */
void comm_task(void *pvParameters)
{
    (void)pvParameters;
    uint8_t tx_buf[PROTO_FRAME_MAX];
    uint32_t tx_len = 0;
    proto_frame_t rx_frame;

    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(10));  /* Poll every 10 ms */

        /* ─── 1. Read available bytes and run state machine ───────────── */
        while (uart_available() > 0) {
            uint8_t byte;
            if (!uart_read_byte(&byte)) break;

            switch (g_rx_state) {
                case SYNC0_WAIT:
                    if (byte == PROTO_SYNC0) {
                        g_frame_buf[0] = byte;
                        g_rx_state = SYNC1_WAIT;
                    }
                    break;

                case SYNC1_WAIT:
                    if (byte == PROTO_SYNC1) {
                        g_frame_buf[1] = byte;
                        g_rx_state = LEN_WAIT;
                    } else {
                        g_rx_state = SYNC0_WAIT;  /* Resync */
                    }
                    break;

                case LEN_WAIT:
                    g_frame_buf[2] = byte;
                    g_expected_len = byte;
                    g_payload_collected = 0;
                    if (g_expected_len == 0) {
                        g_rx_state = CRC_WAIT;
                    } else if (g_expected_len > PROTO_MAX_PAYLOAD) {
                        g_rx_state = SYNC0_WAIT;  /* Invalid length */
                    } else {
                        g_rx_state = PAYLOAD_WAIT;
                    }
                    break;

                case PAYLOAD_WAIT:
                    g_frame_buf[PROTO_HEADER_LEN + g_payload_collected] = byte;
                    g_payload_collected++;
                    if (g_payload_collected >= g_expected_len) {
                        g_rx_state = CRC_WAIT;
                    }
                    break;

                case CRC_WAIT:
                    /* Collect both CRC bytes */
                    {
                        static uint8_t crc_count = 0;
                        static uint16_t crc_val = 0;
                        if (crc_count == 0) {
                            crc_val = byte;
                            crc_count = 1;
                        } else {
                            crc_val |= (uint16_t)byte << 8;
                            crc_count = 0;

                            /* Complete frame — validate CRC and dispatch */
                            uint32_t total_len = PROTO_HEADER_LEN + g_expected_len + PROTO_CRC_LEN;
                            g_frame_buf[PROTO_HEADER_LEN + g_expected_len]     = (uint8_t)(crc_val & 0xFF);
                            g_frame_buf[PROTO_HEADER_LEN + g_expected_len + 1] = (uint8_t)(crc_val >> 8);

                            if (proto_parse_frame(g_frame_buf, total_len, &rx_frame)) {
                                /* Valid frame — ping protection watchdog */
                                protection_comms_ping();

                                /* Dispatch command */
                                uint8_t cmd = rx_frame.cmd;
                                if (cmd < 256 && g_cmd_handlers[cmd]) {
                                    g_cmd_handlers[cmd](&rx_frame, tx_buf, &tx_len);
                                    uart_write(tx_buf, tx_len);
                                } else {
                                    /* Unknown command — send error */
                                    tx_len = proto_build_frame(tx_buf, RSP_ERROR,
                                                               (uint8_t[]){ERR_UNKNOWN_CMD}, 1);
                                    uart_write(tx_buf, tx_len);
                                }
                            }

                            /* Reset state machine */
                            g_rx_state = SYNC0_WAIT;
                        }
                    }
                    break;
            }
        }
    }
}

/* ═══════════════════════════════════════════════════════════════════
 * Command Handlers
 * ═══════════════════════════════════════════════════════════════════ */

static void handle_ping(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len)
{
    (void)rx;
    *tx_len = proto_build_frame(tx_buf, RSP_OK, NULL, 0);
}

static void handle_get_status(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len)
{
    (void)rx;
    *tx_len = proto_build_frame(tx_buf, RSP_STATUS,
                                (const uint8_t*)&g_sys_status,
                                sizeof(g_sys_status));
}

static void handle_get_telemetry(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len)
{
    (void)rx;
    *tx_len = proto_build_frame(tx_buf, RSP_TELEMETRY,
                                (const uint8_t*)&g_telemetry,
                                sizeof(g_telemetry));
}

static void handle_set_mode(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len)
{
    if (rx->payload[0] < MODE_COUNT) {
        el1000_mode_t new_mode = (el1000_mode_t)rx->payload[0];
        modes_switch(&g_modes, new_mode, &g_setpoints);
        *tx_len = proto_build_frame(tx_buf, RSP_OK, NULL, 0);
    } else {
        *tx_len = proto_build_frame(tx_buf, RSP_ERROR,
                                    (uint8_t[]){ERR_INVALID_PARAM}, 1);
    }
}

static void handle_set_setpoint(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len)
{
    if (rx->len >= sizeof(el1000_setpoints_t)) {
        memcpy(&g_setpoints, rx->payload, sizeof(el1000_setpoints_t));
        /* Re-apply setpoints for current mode */
        modes_switch(&g_modes, g_modes.active_mode, &g_setpoints);
        *tx_len = proto_build_frame(tx_buf, RSP_OK, NULL, 0);
    } else {
        *tx_len = proto_build_frame(tx_buf, RSP_ERROR,
                                    (uint8_t[]){ERR_INVALID_PARAM}, 1);
    }
}

static void handle_set_output(const proto_frame_t* rx, uint8_t* tx_buf, uint32_t* tx_len)
{
    if (rx->len >= 1) {
        modes_set_output(&g_modes, rx->payload[0] != 0);
        *tx_len = proto_build_frame(tx_buf, RSP_OK, NULL, 0);
    } else {
        *tx_len = proto_build_frame(tx_buf, RSP_ERROR,
                                    (uint8_t[]){ERR_INVALID_PARAM}, 1);
    }
}

/**
 * TODO:
 *   - Implement remaining handlers: GET_CAL, SET_CAL, SAVE_CAL,
 *     DYN_CONFIG, BAT_CONFIG, START_LOG, STOP_LOG
 *   - Add response timeout tracking
 *   - Add CRC error counters for diagnostics
 *   - Consider DMA-based UART for reduced CPU load
 */
