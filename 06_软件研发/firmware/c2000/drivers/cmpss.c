/**
 * @file    cmpss.c
 * @brief   CMPSS driver implementation.
 */

#include "cmpss.h"

/* ─── Default threshold DAC values (12-bit) ────────────────────────── */
/* These should be loaded from calibration / configuration at runtime.
 * Placeholder values correspond to ~3.0V at ADC input for OVP and ~2.5V for OCP.
 */
#define OVP_DEFAULT_DAC  3723  /* (3.0V / 3.3V) * 4095 */
#define OCP_DEFAULT_DAC  3102  /* (2.5V / 3.3V) * 4095 */

void cmpss_init(void)
{
    /* TODO: Enable CMPSS1 and CMPSS2 clocks (PCLKCR4) */

    /* ─── CMPSS1 (OVP) ────────────────────────────────────────────────── */
    /* TODO: Configure comparator inputs
     *   COMPCTL.COMPDACE = 1;        // Enable DAC
     *   COMPCTL.POL = 0;             // Active high (trip when V+ > V-)
     *   COMPCTL.CINP(positive) = ADC_CH_VLOAD via input mux
     *   COMPCTL.CINN(negative) = internal DAC
     */
    /* TODO: Set DAC threshold
     *   DACHVAL = OVP_DEFAULT_DAC;
     *   DACLVAL = 0;                 // Not using low threshold
     *   COMPDACCTL.DACSOURCE = 1;    // use DACH
     */
    /* TODO: Route output through Input X-BAR to ePWM TZ1 */

    /* ─── CMPSS2 (OCP) ────────────────────────────────────────────────── */
    /* TODO: Mirror above for CMPSS2, route to ePWM TZ2 */
    cmpss_set_ocp_threshold(OCP_DEFAULT_DAC);
}

void cmpss_set_ovp_threshold(uint16_t dac_value)
{
    /* TODO: Cmpss1Regs.DACHVAL = dac_value; */
    (void)dac_value;
}

void cmpss_set_ocp_threshold(uint16_t dac_value)
{
    /* TODO: Cmpss2Regs.DACHVAL = dac_value; */
    (void)dac_value;
}

bool cmpss_is_ovp_tripped(void)
{
    /* TODO: return (Cmpss1Regs.CTLFLG.bit.CTHFLG != 0); */
    return false;
}

bool cmpss_is_ocp_tripped(void)
{
    /* TODO: return (Cmpss2Regs.CTLFLG.bit.CTHFLG != 0); */
    return false;
}

void cmpss_clear_flags(void)
{
    /* TODO: Cmpss1Regs.CTLCLR.bit.CTHCLR = 1;
     *        Cmpss2Regs.CTLCLR.bit.CTHCLR = 1;
     */
}
