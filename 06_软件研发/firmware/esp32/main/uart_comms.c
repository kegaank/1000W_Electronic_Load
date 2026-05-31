/**
 * @file    uart_comms.c
 * @brief   UART communication driver for ESP32 ↔ C2000.
 */

#include "uart_comms.h"
#include "protocol.h"
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "esp_log.h"

static const char *TAG = "UART_COMMS";

#define UART_PORT       UART_NUM_1
#define BUF_SIZE        512
#define TX_TIMEOUT_MS   10

static uart_comms_callback_t g_callback = NULL;

/* ─── Init ─────────────────────────────────────────────────────────── */
void uart_comms_init(void)
{
    /* TODO: Configure UART with ESP-IDF driver API
     *
     * const uart_config_t uart_config = {
     *     .baud_rate  = 921600,
     *     .data_bits  = UART_DATA_8_BITS,
     *     .parity     = UART_PARITY_DISABLE,
     *     .stop_bits  = UART_STOP_BITS_1,
     *     .flow_ctrl  = UART_HW_FLOWCTRL_DISABLE,
     *     .source_clk = UART_SCLK_DEFAULT,
     * };
     * ESP_ERROR_CHECK(uart_param_config(UART_PORT, &uart_config));
     *
     * // Set pins: TX=GPIO17, RX=GPIO18 (adjust for schematic)
     * ESP_ERROR_CHECK(uart_set_pin(UART_PORT, 17, 18, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
     *
     * // Install driver
     * ESP_ERROR_CHECK(uart_driver_install(UART_PORT, BUF_SIZE, BUF_SIZE, 10, NULL, 0));
     */
    ESP_LOGI(TAG, "UART initialized (921600 baud)");
}

/* ─── Transaction ──────────────────────────────────────────────────── */
int uart_comms_transaction(uint8_t cmd, const uint8_t* tx_data, uint32_t tx_len,
                           uint8_t* rx_buf, uint32_t rx_buf_len,
                           uint32_t timeout_ms)
{
    uint8_t frame[PROTO_FRAME_MAX];
    uint32_t frame_len = proto_build_frame(frame, cmd, tx_data, tx_len);
    if (frame_len == 0) return -1;

    /* Send */
    int sent = uart_write_bytes(UART_PORT, (const char*)frame, frame_len);
    if (sent <= 0) return -1;

    /* Wait for and read response */
    /* TODO: Implement proper frame-level read with timeout
     *   int len = uart_read_bytes(UART_PORT, rx_buf, rx_buf_len,
     *                             pdMS_TO_TICKS(timeout_ms));
     */
    (void)rx_buf;
    (void)rx_buf_len;
    (void)timeout_ms;
    return -1; /* Placeholder */
}

void uart_comms_send_async(uint8_t cmd, const uint8_t* data, uint32_t len)
{
    uint8_t frame[PROTO_FRAME_MAX];
    uint32_t frame_len = proto_build_frame(frame, cmd, data, len);
    if (frame_len > 0) {
        uart_write_bytes(UART_PORT, (const char*)frame, frame_len);
    }
}

/* ─── Callback ─────────────────────────────────────────────────────── */
void uart_comms_register_callback(uart_comms_callback_t cb)
{
    g_callback = cb;
}

/* ─── Polling task ─────────────────────────────────────────────────── */
void uart_comms_task(void *pvParameters)
{
    (void)pvParameters;
    TickType_t last_wake = xTaskGetTickCount();

    for (;;) {
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(10));  /* 100 Hz */

        /* TODO: Poll C2000 for telemetry
         *   uint8_t telemetry_buf[sizeof(el1000_telemetry_t)];
         *   int len = uart_comms_transaction(CMD_GET_TELEMETRY, NULL, 0,
         *                                     telemetry_buf, sizeof(telemetry_buf), 10);
         *   if (len > 0) {
         *       el1000_telemetry_t *t = (el1000_telemetry_t *)telemetry_buf;
         *       // Update shared state, notify WebSocket, LVGL, etc.
         *   }
         */
    }
}
