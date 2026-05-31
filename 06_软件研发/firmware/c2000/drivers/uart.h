/**
 * @file    uart.h
 * @brief   SCI-A UART driver for C2000 ↔ ESP32 communication.
 *          Baud rate: 921600, 8N1, binary protocol framing.
 */

#ifndef UART_H
#define UART_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── UART buffer sizes ────────────────────────────────────────────── */
#define UART_RX_BUF_SIZE  256
#define UART_TX_BUF_SIZE  256

/**
 * @brief  Initialize SCI-A UART.
 *
 * Configures:
 *   - Baud: 921600 (BRR = SYSCLK / (8 * 921600) - 1 ≈ 15 @ 120 MHz)
 *   - 8 data bits, no parity, 1 stop bit (8N1)
 *   - FIFO mode (16-byte FIFOs)
 *   - RX interrupt on non-empty FIFO
 *
 * TODO: Set SCIA base address
 * TODO: Configure SCICTL1, SCICTL2, SCICCR, SCIHBAUD, SCILBAUD
 * TODO: Enable FIFO (SCIFFTX, SCIFFRX, SCIFFCT)
 * TODO: Route RX interrupt through PIE (group 9)
 * TODO: Configure GPIO for SCI-A (SCIRXDA, SCITXDA on appropriate pins)
 */
void uart_init(void);

/**
 * @brief  Send a byte via UART (blocking poll).
 * @param  data  Byte to transmit.
 *
 * TODO: Wait for TX FIFO ready bit (SCICTL2.TXRDY), write SCITXBUF
 */
void uart_putc(uint8_t data);

/**
 * @brief  Send a byte via UART (non-blocking FIFO).
 * @param  data  Byte to transmit.
 * @return true if written, false if FIFO full.
 *
 * TODO: Check TXFIFO level; write if space available
 */
bool uart_putc_nb(uint8_t data);

/**
 * @brief  Send a buffer of bytes (blocking).
 * @param  data  Pointer to data buffer
 * @param  len   Number of bytes to send
 */
void uart_write(const uint8_t* data, uint32_t len);

/**
 * @brief  Get the number of bytes waiting in RX buffer.
 * @return Count of received bytes not yet read.
 */
uint32_t uart_available(void);

/**
 * @brief  Read one byte from RX buffer.
 * @param  data  Pointer to receive the byte
 * @return true if a byte was read, false if buffer empty.
 */
bool uart_read_byte(uint8_t* data);

/**
 * @brief  Flush the RX buffer (discard all pending bytes).
 */
void uart_flush_rx(void);

/**
 * @brief  Check if UART TX is idle (all bytes sent).
 * @return true if TX complete.
 */
bool uart_tx_idle(void);

/**
 * ─── UART RX ISR ─────────────────────────────────────────────────────
 *
 * Called by PIE on SCI-A RX FIFO interrupt.
 * Reads bytes from SCIRXBUF into the circular RX buffer.
 *
 * interrupt void uart_rx_isr(void)
 * {
 *     while (!SCIFFRX.RXFFST empty) {
 *         uint8_t byte = SciaRegs.SCIRXBUF.bit.RXDT;
 *         // store in circular buffer
 *     }
 *     PieCtrlRegs.PIEACK.all |= (1 << 8);  // group 9 ack
 * }
 */

#ifdef __cplusplus
}
#endif

#endif /* UART_H */
