/**
 * @file    timer.h
 * @brief   ePWM timer helpers for C2000 F28E12x.
 *          General-purpose timer / delay / period measurement using
 *          ePWM time-base counters.
 */

#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Blocking microsecond delay using ePWM counter or CPU timer.
 * @param  us  Microseconds to delay.
 *
 * TODO: Implement using CPU Timer 0:
 *   ConfigCpuTimer(&CpuTimer0, 120, us);  // 120 MHz
 *   CpuTimer0Regs.TCR.bit.TSS = 0;        // start
 *   while (CpuTimer0Regs.TCR.bit.TIF == 0) {}
 *   CpuTimer0Regs.TCR.bit.TSS = 1;        // stop
 */
void timer_delay_us(uint32_t us);

/**
 * @brief  Blocking millisecond delay.
 * @param  ms  Milliseconds to delay.
 */
static inline void timer_delay_ms(uint32_t ms)
{
    for (uint32_t i = 0; i < ms; i++) {
        timer_delay_us(1000);
    }
}

/**
 * @brief  Start a microsecond-accurate timer for period measurement.
 *
 * TODO: Capture ePWM counter value as start reference
 */
void timer_start_measure(void);

/**
 * @brief  Stop measurement timer and return elapsed microseconds.
 * @return Elapsed time in microseconds since last timer_start_measure().
 *
 * TODO: Capture ePWM counter, compute delta, convert to µs
 */
uint32_t timer_stop_measure_us(void);

/**
 * @brief  Get the raw free-running counter value of ePWM1.
 * @return Current TBCTR value.
 *
 * Useful for timestamping telemetry samples.
 * TODO: return EPwm1Regs.TBCTR;
 */
uint16_t timer_get_tbctr(void);

/**
 * @brief  Convert timer counts to microseconds.
 * @param  counts  Timer count ticks
 * @return Time in microseconds (fractional for sub-µs accuracy).
 *
 * TODO: Use TBPRD and clock divider to compute conversion factor
 */
float timer_counts_to_us(uint16_t counts);

#ifdef __cplusplus
}
#endif

#endif /* TIMER_H */
