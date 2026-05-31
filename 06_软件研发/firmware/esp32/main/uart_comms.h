/**
 * @file    uart_comms.h
 * @brief   UART communication driver for ESP32 ↔ C2000.
 */

#ifndef UART_COMMS_H
#define UART_COMMS_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Initialize UART0 for communication with C2000.
 *         Baud: 921600, 8N1, hardware flow control disabled.
 *
 * TODO: Configure uart_config_t with ESP-IDF driver
 */
void uart_comms_init(void);

/**
 * @brief  Send a command frame to C2000 and wait for response.
 * @param  cmd        Command ID
 * @param  tx_data    Payload to send (may be NULL)
 * @param  tx_len     Payload length
 * @param  rx_buf     Buffer for response payload
 * @param  rx_buf_len Max bytes to read
 * @param  timeout_ms Timeout in milliseconds
 * @return Response payload length on success, -1 on error.
 */
int uart_comms_transaction(uint8_t cmd, const uint8_t* tx_data, uint32_t tx_len,
                           uint8_t* rx_buf, uint32_t rx_buf_len,
                           uint32_t timeout_ms);

/**
 * @brief  Send a frame asynchronously (fire-and-forget).
 * @param  cmd     Command ID
 * @param  data    Payload
 * @param  len     Payload length
 */
void uart_comms_send_async(uint8_t cmd, const uint8_t* data, uint32_t len);

/**
 * @brief  Register a callback for unsolicited frames from C2000.
 *         (e.g., telemetry push at 100 Hz)
 */
typedef void (*uart_comms_callback_t)(uint8_t cmd, const uint8_t* data, uint32_t len);
void uart_comms_register_callback(uart_comms_callback_t cb);

/**
 * @brief  Task: periodically polls C2000 for telemetry and status.
 *         Runs on core 0 at 100 Hz.
 */
void uart_comms_task(void *pvParameters);

#ifdef __cplusplus
}
#endif

#endif /* UART_COMMS_H */
