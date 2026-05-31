/**
 * @file    protocol.h
 * @brief   Shared UART protocol definition between C2000 and ESP32.
 *
 * Frame format (binary, little-endian):
 *   [0xAA] [0x55] [len] [cmd_id] [payload...] [crc16_lo] [crc16_hi]
 *   Header: 2 bytes (sync: 0xAA 0x55)
 *   Len:    1 byte  (payload bytes, excludes header/len/crc)
 *   Cmd:    1 byte  (command/response ID)
 *   Payload: 0–251 bytes
 *   CRC16:  2 bytes (CCITT, over len+cmd+payload)
 *
 * Max frame size: 2 + 1 + 1 + 251 + 2 = 257 bytes.
 */

#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Protocol Constants ──────────────────────────────────────────── */

#define PROTO_SYNC0         0xAAu
#define PROTO_SYNC1         0x55u
#define PROTO_MAX_PAYLOAD   251u
#define PROTO_HEADER_LEN    4u    /* sync0 + sync1 + len + cmd */
#define PROTO_CRC_LEN       2u
#define PROTO_FRAME_MAX     (PROTO_HEADER_LEN + PROTO_MAX_PAYLOAD + PROTO_CRC_LEN)

/* ─── Command IDs (Host → C2000) ──────────────────────────────────── */

typedef enum {
    /* System */
    CMD_PING            = 0x01,
    CMD_GET_STATUS      = 0x02,
    CMD_GET_TELEMETRY   = 0x03,
    CMD_SET_MODE        = 0x04,
    CMD_SET_SETPOINT    = 0x05,
    CMD_SET_OUTPUT      = 0x06,   /* payload: 1=ON, 0=OFF */
    CMD_GET_CAL         = 0x07,
    CMD_SET_CAL         = 0x08,
    CMD_SAVE_CAL        = 0x09,

    /* Advanced */
    CMD_DYN_CONFIG      = 0x10,
    CMD_BAT_CONFIG      = 0x11,
    CMD_START_LOG       = 0x12,
    CMD_STOP_LOG        = 0x13,

    /* Responses (C2000 → Host) */
    RSP_OK              = 0x80,
    RSP_ERROR           = 0x81,
    RSP_STATUS          = 0x82,
    RSP_TELEMETRY       = 0x83,
    RSP_CAL_DATA        = 0x84,
    RSP_LOG_DATA        = 0x85,
} proto_cmd_t;

/* ─── Error Codes ──────────────────────────────────────────────────── */

typedef enum {
    ERR_NONE            = 0x00,
    ERR_UNKNOWN_CMD     = 0x01,
    ERR_INVALID_PARAM   = 0x02,
    ERR_BUSY            = 0x03,
    ERR_PROTECTION      = 0x04,
    ERR_CAL_INVALID     = 0x05,
    ERR_CRC             = 0x06,
    ERR_TIMEOUT         = 0x07,
} proto_err_t;

/* ─── Frame Structure ──────────────────────────────────────────────── */

typedef struct __attribute__((packed)) {
    uint8_t  sync0;         /**< 0xAA */
    uint8_t  sync1;         /**< 0x55 */
    uint8_t  len;           /**< Payload length */
    uint8_t  cmd;           /**< Command/response ID */
    uint8_t  payload[PROTO_MAX_PAYLOAD]; /**< Payload data */
    uint16_t crc;           /**< CRC-16 CCITT */
} proto_frame_t;

/* ─── CRC-16 ───────────────────────────────────────────────────────── */

uint16_t proto_crc16(const uint8_t* data, uint32_t len);

/* ─── Frame building helpers ───────────────────────────────────────── */

/**
 * @brief Build a protocol frame in the given buffer.
 * @param buf       Output buffer (must be >= PROTO_FRAME_MAX bytes)
 * @param cmd       Command/response ID
 * @param payload   Payload data (may be NULL if len==0)
 * @param len       Payload length (max PROTO_MAX_PAYLOAD)
 * @return Total frame length on success, 0 on error.
 */
uint32_t proto_build_frame(uint8_t* buf, uint8_t cmd,
                           const uint8_t* payload, uint32_t len);

/**
 * @brief Validate and parse an incoming frame.
 * @param buf       Raw received buffer
 * @param len       Number of bytes in buf
 * @param frame     Output parsed frame structure
 * @return 1 if valid, 0 if invalid/crc error.
 */
int proto_parse_frame(const uint8_t* buf, uint32_t len, proto_frame_t* frame);

#ifdef __cplusplus
}
#endif

#endif /* PROTOCOL_H */
