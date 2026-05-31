/**
 * @file    hrpwm.c
 * @brief   HRPWM driver implementation.
 */

#include "hrpwm.h"

/* ─── Module state ─────────────────────────────────────────────────── */
static uint16_t g_epwm1_period = 0;
static uint16_t g_epwm2_period = 0;

/* ─── Register offsets (F28E12x) ───────────────────────────────────── */
/* TODO: Verify register map against F28E12x datasheet.
 *       These are representative — adjust for your specific device:

 * #define EPWM1_BASE      0x00006800UL
 * #define EPWM2_BASE      0x00006820UL
 * #define HRPWM1_BASE     0x00006880UL
 */

/* ─── Init ─────────────────────────────────────────────────────────── */
void hrpwm_init(void)
{
    /* TODO: Enable ePWM1-2 clocks in PCLKCR0/1 */

    /* ePWM1 — Main load channel */
    /* TODO: Set TBCTL (free/soft, clock divider, phase direction) */
    /*   TBCTL = FREE_SOFT_STOP | CLKDIV_DIV1 | HSPCLKDIV_DIV1 | PHSDIR_UP; */

    /* TODO: Set TBPRD = 2400 for 25 kHz @ 120 MHz SYSCLK */
    /*   TBPRD = 2400; */

    /* TODO: Set counter to up-count mode */
    /*   TBCTL.CTRMODE = TB_UPDOWN;  // up-down for complementary */

    /* TODO: Configure compare actions:
     *   CMPA up: set EPWM1A;       CMPA down: clear EPWM1A
     *   CMPB up: clear EPWM1B;     CMPB down: set EPWM1B
     */

    /* TODO: Configure dead-band:
     *   DBCTL = OUT_MODE | RED_ENABLE | FED_ENABLE | POLSEL_ACTIVE_HI;
     *   DBFED = 24;  // 200 ns @ 120 MHz => 24 cycles
     *   DBRED = 24;
     */

    /* TODO: Configure trip-zone (both ePWM1 + ePWM2):
     *   TZSEL = DCBEVT1 | DCBEVT2;  // TZ1 from CMPSS1, TZ2 from CMPSS2
     *   TZCTL = TZA_HIZ | TZB_HIZ;  // high-impedance on trip
     *   TZEINT = OST;
     */

    /* TODO: Enable HRPWM on ePWM1A:
     *   HRCNFG = HRLOAD | AUTOCONF | SELOUTB | CTL_CMPA | HRPE;
     *   HRMSTEP = computed MEP steps per SYSCLK cycle
     *   HRPCTL = CHPEN;
     */

    g_epwm1_period = 2400;

    /* ePWM2 — Aux channel */
    /* TODO: Mirror ePWM1 config for ePWM2, or configure independently */
    g_epwm2_period = 2400;

    /* TODO: Enable PWM outputs on GPIO0-3 (EPWM1A/B, EPWM2A/B) */
}

/* ─── Duty cycle setters ───────────────────────────────────────────── */
void hrpwm_set_duty_epwm1(uint16_t duty_cycles)
{
    /* TODO: Write CMPA = duty_cycles (integer part)
     *       Write CMPAHR = (fraction * MEP_SCALE) for HRPWM step
     *       Ensure HRCNFG.CTL = CTL_CMPA so HRPWM uses CMPAHR
     *
     * Note: If using up-count mode, active high => duty = CMPA/TBPRD
     *       If using up-down count, duty = CMPA/(TBPRD/2)
     */
}

void hrpwm_set_duty_epwm2(uint16_t duty_cycles)
{
    /* TODO: Same as above for ePWM2 */
}

/* ─── Shutdown / Recovery ──────────────────────────────────────────── */
void hrpwm_force_shutdown(void)
{
    /* TODO: Write TZFORCE to simulate trip event
     *   EPwm1Regs.TZFRC.bit.OST = 1;
     *   EPwm2Regs.TZFRC.bit.OST = 1;
     */
}

void hrpwm_trip_recover(void)
{
    /* TODO: Clear trip-zone flags
     *   EPwm1Regs.TZCLR.bit.OST = 1;
     *   EPwm1Regs.TZCLR.bit.CBC = 1;
     *   EPwm1Regs.TZCLR.bit.INT = 1;
     *   (repeat for ePWM2)
     */
}

uint16_t hrpwm_get_period(void)
{
    return g_epwm1_period;
}
