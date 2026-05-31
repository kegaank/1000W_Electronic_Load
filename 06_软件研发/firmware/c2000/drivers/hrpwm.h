/**
 * @file    hrpwm.h
 * @brief   HRPWM driver for C2000 F28E12x.
 *          ePWM1-2 configured for 25 kHz complementary PWM with
 *          high-resolution MEP (micro-edge positioner) ~150 ps steps.
 */

#ifndef HRPWM_H
#define HRPWM_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Public API ───────────────────────────────────────────────────── */

/**
 * @brief  Initialize HRPWM modules (ePWM1, ePWM2).
 *
 * Configures:
 *   - Time-base: 25 kHz (TBPRD = SYSCLK / (2 * 25,000))
 *   - HRPWM: MEP enabled on ePWM1A, ePWM2A
 *   - Dead-band: 200 ns rising/falling delay
 *   - Trip-zone: TZ1 (CMPSS1 OVP), TZ2 (CMPSS2 OCP)
 *   - Complementary PWM pair on ePWM1A/B
 *
 * TODO: Set TBPRD = 120e6 / (2 * 25000) = 2400
 * TODO: Configure dead-band module (DBCTL, DBFED, DBRED)
 * TODO: Configure trip-zone (TZSEL, TZCTL) for one-shot on fault
 * TODO: Enable HRPWM on channel A (HRCNFG)
 * TODO: Configure MEP step scale (HRMSTEP, HRPCTL)
 */
void hrpwm_init(void);

/**
 * @brief  Set the PWM duty cycle for ePWM1 (main load channel).
 * @param  duty_cycles  Raw compare value (0 to TBPRD).
 *                      Use HRPWM for fractional cycle adjustment.
 *
 * TODO: Write CMPA:CMPAHR with MEP steps for ~150 ps resolution
 */
void hrpwm_set_duty_epwm1(uint16_t duty_cycles);

/**
 * @brief  Set the PWM duty cycle for ePWM2 (secondary/aux channel).
 * @param  duty_cycles  Raw compare value (0 to TBPRD).
 */
void hrpwm_set_duty_epwm2(uint16_t duty_cycles);

/**
 * @brief  Force all PWM outputs to a safe state (shoot-through protect).
 *         Called by protection task on fault.
 *
 * TODO: Set TZFORCE with TZA = TZB = high-impedance
 */
void hrpwm_force_shutdown(void);

/**
 * @brief  Clear trip-zone latch and re-enable PWM output.
 *
 * TODO: Write TZCLR register
 */
void hrpwm_trip_recover(void);

/**
 * @brief  Get the current PWM period (TBPRD) in timer counts.
 */
uint16_t hrpwm_get_period(void);

#ifdef __cplusplus
}
#endif

#endif /* HRPWM_H */
