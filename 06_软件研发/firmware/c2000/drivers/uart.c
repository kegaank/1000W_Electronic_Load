/**
 * @file    uart.c
 * @brief   SCI-A UART driver implementation.
 */

#include "uart.h"
#include <string.h>

/* ─── Circular RX buffer ───────────────────────────────────────────── */
static uint8_t  g_rx_buf[UART_RX_BUF_SIZE];
static uint32_t g_rx_head = 0;
static uint32_t g_rx_tail = 0;
static uint32_t g_rx_count = 0;

/* ─── TX busy flag ─────────────────────────────────────────────────── */
static volatile bool g_tx_busy = false;

void uart_init(void)
{
    g_rx_head  = 0;
    g_rx_tail  = 0;
    g_rx_count = 0;
    g_tx_busy  = false;

    /* TODO: Enable SCI-A clock (PCLKCR0) */

    /* TODO: Configure GPIO for SCI-A:
     *   GPIO28 = SCIRXDA (input, pullup)
     *   GPIO29 = SCITXDA (output, pullup)
     */

    /* TODO: Reset SCI-A
     *   SciaRegs.SCICTL1.bit.SWRESET = 0;
     *   delay_ms(1);
     */

    /* TODO: Configure UART frame: 8N1
     *   SciaRegs.SCICCR.all = 0x0007;
     *   // 1 stop bit, no parity, 8 data bits, async, idle-line proto
     */

    /* TODO: Set baud rate for 921600 @ 120 MHz
     *   BRR = (120e6 / (8 * 921600)) - 1 = 15.27 => 15
     *   SciaRegs.SCIHBAUD = 0x0000;
     *   SciaRegs.SCILBAUD = 15;
     */

    /* TODO: Enable FIFO mode
     *   SciaRegs.SCIFFTX.all = 0xE040;  // enable TX FIFO, clear flags
     *   SciaRegs.SCIFFRX.all = 0x2040;  // enable RX FIFO, clear flags, 16-level
     *   SciaRegs.SCIFFCT.all = 0x00;    // no delay
     */

    /* TODO: Enable TX/RX and interrupt
     *   SciaRegs.SCICTL1.all = 0x0023;  // enable RX, TX, sleep
     *   SciaRegs.SCIFFRX.bit.RXFFIENA = 1; // RX FIFO interrupt
     *   SciaRegs.SCIFFTX.bit.TXFIFOXRESET = 1;
     *   SciaRegs.SCIFFRX.bit.RXFIFORESET = 1;
     */

    /* TODO: Route interrupt: PIE group 9, vector 1
     *   PieCtrlRegs.PIEIER9.bit.INTx1 = 1;
     */

    /* TODO: Finalize
     *   SciaRegs.SCICTL1.bit.SWRESET = 1;
     */
}

/* ─── TX (blocking) ────────────────────────────────────────────────── */
void uart_putc(uint8_t data)
{
    /* TODO: Wait for TX buffer ready
     *   while (SciaRegs.SCICTL2.bit.TXRDY == 0) {}
     *   SciaRegs.SCITXBUF = data;
     */
}

bool uart_putc_nb(uint8_t data)
{
    /* TODO: Check TXFFST in SCIFFTX, return false if full */
    (void)data;
    return false;
}

void uart_write(const uint8_t* data, uint32_t len)
{
    g_tx_busy = true;
    for (uint32_t i = 0; i < len; i++) {
        uart_putc(data[i]);
    }
    g_tx_busy = false;
}

uint32_t uart_available(void)
{
    uint32_t count;
    /* TODO: Disable interrupt for atomic read */
    count = g_rx_count;
    /* TODO: Restore interrupt */
    return count;
}

bool uart_read_byte(uint8_t* data)
{
    if (g_rx_count == 0) {
        return false;
    }
    *data = g_rx_buf[g_rx_tail];
    g_rx_tail = (g_rx_tail + 1) % UART_RX_BUF_SIZE;
    /* TODO: Disable interrupt for atomic decrement */
    g_rx_count--;
    /* TODO: Restore interrupt */
    return true;
}

void uart_flush_rx(void)
{
    /* TODO: Disable interrupt */
    g_rx_head  = 0;
    g_rx_tail  = 0;
    g_rx_count = 0;
    /* TODO: Restore interrupt */
}

bool uart_tx_idle(void)
{
    return !g_tx_busy;
}

/**
 * ─── UART RX ISR (PIE group 9, vector 1) ───────────────────────────
 *
 * interrupt void uart_rx_isr(void)
 * {
 *     uint16_t status = SciaRegs.SCIFFRX.all;
 *     while ((status & 0x3F) > 0) {  // RXFFST bits
 *         uint8_t byte = SciaRegs.SCIRXBUF.all & 0xFF;
 *         g_rx_buf[g_rx_head] = byte;
 *         g_rx_head = (g_rx_head + 1) % UART_RX_BUF_SIZE;
 *         g_rx_count++;
 *         if (g_rx_count > UART_RX_BUF_SIZE) {
 *             g_rx_count = UART_RX_BUF_SIZE; // drop oldest
 *             g_rx_tail = (g_rx_tail + 1) % UART_RX_BUF_SIZE;
 *         }
 *         status = SciaRegs.SCIFFRX.all;  // re-read
 *     }
 *     SciaRegs.SCIFFRX.bit.RXFFOVRCLR = 1;  // clear overflow
 *     PieCtrlRegs.PIEACK.all |= (1 << 8);    // group 9 ack
 * }
 */
