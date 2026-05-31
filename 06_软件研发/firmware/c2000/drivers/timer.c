/**
 * @file    timer.c
 * @brief   ePWM timer helper implementation.
 */

#include "timer.h"

/* ─── Measurement state ────────────────────────────────────────────── */
static uint16_t g_measure_start = 0;

/* ─── Delays ───────────────────────────────────────────────────────── */
void timer_delay_us(uint32_t us)
{
    /* TODO: Use CPU Timer 0 for blocking delay.
     *
     *   CpuTimer0Regs.TPR.all  = 0;
     *   CpuTimer0Regs.TPRH.all = 0;
     *   CpuTimer0Regs.TIM.all  = 0;
     *   CpuTimer0Regs.TCR.bit.TSS = 1;  // stop
     *   // reload with (SYSCLK / 1000000) * us
     *   uint32_t reload = (120000000UL / 1000000UL) * us;
     *   CpuTimer0Regs.PRD.all = reload;
     *   CpuTimer0Regs.TCR.bit.TRB = 1;      // reload
     *   CpuTimer0Regs.TCR.bit.TIF = 0;      // clear interrupt flag
     *   CpuTimer0Regs.TCR.bit.TSS = 0;      // start
     *   while (CpuTimer0Regs.TCR.bit.TIF == 0) {} // wait
     *   CpuTimer0Regs.TCR.bit.TSS = 1;      // stop
     */
    (void)us;
}

/* ─── Measurement ──────────────────────────────────────────────────── */
void timer_start_measure(void)
{
    /* TODO: g_measure_start = EPwm1Regs.TBCTR; */
    g_measure_start = 0;
}

uint32_t timer_stop_measure_us(void)
{
    /* TODO: uint16_t now = EPwm1Regs.TBCTR;
     *        uint16_t delta;
     *        if (now >= g_measure_start)
     *            delta = now - g_measure_start;
     *        else
     *            delta = (EPwm1Regs.TBPRD - g_measure_start) + now;
     *
     *        // Convert counts to µs:
     *        // 25 kHz period = 2400 counts, period = 40 µs
     *        // Each count = 40e-6 / 2400 ≈ 0.01667 µs
     *        return (uint32_t)((float)delta * 0.01667f);
     */
    return 0;
}

uint16_t timer_get_tbctr(void)
{
    /* TODO: return EPwm1Regs.TBCTR; */
    return 0;
}

float timer_counts_to_us(uint16_t counts)
{
    /* At 25 kHz ePWM with TBPRD=2400 and up-down count:
     *   Period = 40 µs = 2 * TBPRD counts
     *   So 1 count = 40e-6 / (2 * 2400) ≈ 8.33 ns
     */
    const float US_PER_COUNT = 0.008333f;  /* ~8.33 ns */
    return (float)counts * US_PER_COUNT;
}
