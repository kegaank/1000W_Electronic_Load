/**
 * @file    adc.h
 * @brief   ADC driver for C2000 F28E12x.
 *          Dual ADC module (A/B), 13-channel sequential sampling
 *          triggered by ePWM1 SOC at 860 Hz.
 */

#ifndef ADC_H
#define ADC_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Number of ADC channels sampled */
#define ADC_NUM_CHANNELS  13

/* ─── Channel mapping ──────────────────────────────────────────────── */
typedef enum {
    ADC_CH_VBATT   = 0,   /**< Battery voltage (monitor) */
    ADC_CH_IBATT   = 1,   /**< Battery current (shunt) */
    ADC_CH_VLOAD   = 2,   /**< Load voltage (main) */
    ADC_CH_ILOAD   = 3,   /**< Load current (shunt) */
    ADC_CH_VREF    = 4,   /**< Internal Vref monitor */
    ADC_CH_IREF    = 5,   /**< Current ref DAC output */
    ADC_CH_TEMP1   = 6,   /**< Heatsink NTC thermistor */
    ADC_CH_TEMP2   = 7,   /**< Secondary temp sensor */
    ADC_CH_AUX1    = 8,   /**< Spare / expansion */
    ADC_CH_AUX2    = 9,
    ADC_CH_AUX3    = 10,
    ADC_CH_PSU_MON = 11,  /**< Internal PSU rail */
    ADC_CH_VSET    = 12,  /**< Voltage setpoint DAC feedback */
    ADC_CH_COUNT
} adc_channel_t;

/* ─── Public API ───────────────────────────────────────────────────── */

/**
 * @brief  Initialize ADC modules A and B.
 *
 * Configures:
 *   - ADC clock: ADCCLK derived from SYSCLK (e.g., 50 MHz max)
 *   - Resolution: 12-bit (or 16-bit if available on F28E12x)
 *   - Sample window: S+H duration per channel
 *   - SOC triggers: ePWM1 SOCA/C for 860 Hz sampling
 *   - Interrupt: ADCINT1 on end-of-sequence
 *
 * TODO: Set ADCTRL[1 TEMPS], ADCCLKPS for ADC clock ≤ 50 MHz
 * TODO: Configure ADCSAMPLEMODE for each channel
 * TODO: Configure SOC priority (round-robin or sequential)
 * TODO: Enable ADCIE for EOC interrupt
 */
void adc_init(void);

/**
 * @brief  Read the latest raw ADC result for a channel.
 * @param  ch  Channel enum (0–12)
 * @return 12-bit (or 16-bit) raw ADC value.
 *
 * TODO: Access AdcResult.ADCRESULT[x] register
 */
uint16_t adc_read_raw(adc_channel_t ch);

/**
 * @brief  Read and scale a channel to engineering units (volts).
 * @param  ch  Channel to read
 * @return Voltage reading in volts, referenced to 0–3.3 V input range.
 *
 * Conversion: V = (raw * VREF) / (2^resolution - 1)
 *
 * TODO: Apply per-channel calibration offsets/gains from g_cal
 */
float adc_read_voltage(adc_channel_t ch);

/**
 * @brief  Read the load current, applying shunt gain.
 * @return Current in amperes.
 *
 * TODO: Multiply ADC reading by shunt gain (e.g., 50 mV/A)
 *       and amplifier gain factor per hardware design.
 */
float adc_read_current(void);

/**
 * @brief  Read thermistor channel and convert to °C.
 * @param  ch  Temperature sensor channel (ADC_CH_TEMP1 or _TEMP2)
 * @return Temperature in degrees Celsius.
 *
 * TODO: Implement Steinhart-Hart NTC conversion or lookup table
 */
float adc_read_temperature(adc_channel_t ch);

/**
 * @brief  Read the internal PSU monitoring voltage.
 * @return PSU voltage in millivolts.
 *
 * TODO: Scale with resistive divider ratio (e.g., 4:1 from 12V rail)
 */
uint16_t adc_read_psu_mv(void);

/**
 * @brief  Get pointer to raw ADC result buffer.
 *         Updated by ADC ISR on each conversion sequence.
 */
const uint16_t* adc_get_buffer(void);

/**
 * @brief  Calibrate an ADC channel (offset & gain).
 * @param  ch      Channel to calibrate
 * @param  offset  Zero-input offset in ADC counts
 * @param  gain    Scale factor (1.0 = ideal)
 *
 * TODO: Store in per-channel cal table
 */
void adc_calibrate_channel(adc_channel_t ch, int16_t offset, float gain);

#ifdef __cplusplus
}
#endif

#endif /* ADC_H */
