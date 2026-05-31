/**
 * @file    cmpss.h
 * @brief   CMPSS (Comparator Subsystem) driver for C2000 F28E12x.
 *
 * Provides hardware-level over-voltage (OVP) and over-current (OCP)
 * protection. Comparators directly trip the ePWM TZ inputs for
 * sub-microsecond fault response.
 */

#ifndef CMPSS_H
#define CMPSS_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── CMPSS module assignment ──────────────────────────────────────── */
#define CMPSS_OVP   0   /**< CMPSS1 — Over-voltage protection */
#define CMPSS_OCP   1   /**< CMPSS2 — Over-current protection */

/* ─── Thresholds (raw DAC values) ──────────────────────────────────── */

/**
 * @brief  Initialize CMPSS modules.
 *
 * Configures:
 *   - CMPSS1: Vload ADC input to DACHx, reference from DACx
 *   - CMPSS2: Iload ADC input to DACHx, reference from DACx
 *   - Trip outputs routed to ePWM TZ1 / TZ2
 *   - Digital filter for noise rejection (optional)
 *
 * TODO: Set DACxVAL (comparator threshold) for each module
 * TODO: Configure comparator positive/negative input mux
 *       (COMPDACCTL, COMPCTL)
 * TODO: Route CMPSSx output to ePWM trip-zone (Input X-BAR)
 * TODO: Configure digital filter (CTRIPHFILCTL, CTRIPLFILCTL)
 */
void cmpss_init(void);

/**
 * @brief  Set the over-voltage protection threshold.
 * @param  dac_value  12-bit DAC value (0–4095) corresponding to V threshold.
 *
 * TODO: Write CMPSS1 DACxVAL register
 */
void cmpss_set_ovp_threshold(uint16_t dac_value);

/**
 * @brief  Set the over-current protection threshold.
 * @param  dac_value  12-bit DAC value (0–4095) corresponding to I threshold.
 *
 * TODO: Write CMPSS2 DACxVAL register
 */
void cmpss_set_ocp_threshold(uint16_t dac_value);

/**
 * @brief  Read whether OVP comparator is currently tripped.
 * @return true if Vload > OVP threshold.
 *
 * TODO: Read CMPSS1 CTLFLG register
 */
bool cmpss_is_ovp_tripped(void);

/**
 * @brief  Read whether OCP comparator is currently tripped.
 * @return true if Iload > OCP threshold.
 *
 * TODO: Read CMPSS2 CTLFLG register
 */
bool cmpss_is_ocp_tripped(void);

/**
 * @brief  Clear latched trip flags after a fault event.
 *
 * TODO: Write CMPSSx CTLCLR register
 */
void cmpss_clear_flags(void);

#ifdef __cplusplus
}
#endif

#endif /* CMPSS_H */
