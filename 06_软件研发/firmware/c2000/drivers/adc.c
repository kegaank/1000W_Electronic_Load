/**
 * @file    adc.c
 * @brief   ADC driver implementation.
 */

#include "adc.h"

/* ─── Per-channel calibration data ─────────────────────────────────── */
typedef struct {
    int16_t offset;     /**< ADC counts offset at zero input */
    float   gain;       /**< ADC gain correction factor */
    float   vref;       /**< Voltage reference for this channel (V) */
} adc_cal_t;

static adc_cal_t g_adc_cal[ADC_NUM_CHANNELS];
static uint16_t  g_adc_buffer[ADC_NUM_CHANNELS];  /**< Latest results */

/* Default VREF = 3.3 V for all channels */
static const float ADC_VREF = 3.3f;
static const uint32_t ADC_RESOLUTION = 4096;  /* 12-bit */

/* ─── Init ─────────────────────────────────────────────────────────── */
void adc_init(void)
{
    int i;

    /* Initialize calibration defaults */
    for (i = 0; i < ADC_NUM_CHANNELS; i++) {
        g_adc_cal[i].offset = 0;
        g_adc_cal[i].gain   = 1.0f;
        g_adc_cal[i].vref   = ADC_VREF;
        g_adc_buffer[i]     = 0;
    }

    /* TODO: Enable ADC clocks (PCLKCR0) */
    /* TODO: Power-up ADC */
    /*   AdcRegs.ADCCTL1.bit.ADCPWDN = 1; */
    /*   delay_us(1000); */

    /* TODO: Configure ADC clock prescaler
     *   AdcRegs.ADCCTL2.bit.CLKDIV2EN = 1;  // enable /2
     *   AdcRegs.ADCCTL2.bit.PRESCALE = 3;   // ADCCLK = SYSCLK / 4
     */

    /* TODO: Set resolution
     *   AdcRegs.ADCCTL1.bit.RES = 0;  // 0=12-bit, 1=16-bit
     */

    /* TODO: Configure SOC triggers for sequential sampling
     *   For each channel i:
     *     AdcRegs.ADCSOCxCTL.bit.TRIGSEL = 0;  // ePWM1 SOCA
     *     AdcRegs.ADCSOCxCTL.bit.CHSEL   = i;
     *     AdcRegs.ADCSOCxCTL.bit.ACQPS   = 15; // acquire window
     */

    /* TODO: Configure interrupt
     *   AdcRegs.ADCINT1SEL.bit.INT1SEL = 13;  // EOC13 = end of seq
     *   AdcRegs.ADCINTSOCSEL1.bit.SOC0  = 0;  // skip
     *   PieCtrlRegs.PIEIER1.bit.INTx6   = 1;  // ADCINT1 in PIE group 1
     */
}

/* ─── Raw read ─────────────────────────────────────────────────────── */
uint16_t adc_read_raw(adc_channel_t ch)
{
    if (ch >= ADC_NUM_CHANNELS) return 0;
    return g_adc_buffer[ch];
}

/* ─── Scaled read ──────────────────────────────────────────────────── */
float adc_read_voltage(adc_channel_t ch)
{
    if (ch >= ADC_NUM_CHANNELS) return 0.0f;
    uint16_t raw = g_adc_buffer[ch];
    adc_cal_t *cal = &g_adc_cal[ch];
    float corrected = (float)((int32_t)raw + cal->offset) * cal->gain;
    if (corrected < 0.0f) corrected = 0.0f;
    return (corrected / (float)(ADC_RESOLUTION - 1)) * cal->vref;
}

float adc_read_current(void)
{
    float v_shunt = adc_read_voltage(ADC_CH_ILOAD);
    /* TODO: Apply shunt resistor gain.
     *  Example: shunt = 0.001 Ω (1 mΩ), amplifier gain = 50x
     *  Then 1 A => 50 mV across amplifier output
     *  I = V_shunt_voltage / (shunt_ohms * amp_gain)
     */
    const float SHUNT_OHMS    = 0.001f;   /* 1 mΩ shunt */
    const float AMP_GAIN      = 50.0f;    /* Differential amplifier gain */
    return v_shunt / (SHUNT_OHMS * AMP_GAIN);
}

float adc_read_temperature(adc_channel_t ch)
{
    float v = adc_read_voltage(ch);
    /* TODO: Implement Steinhart-Hart equation with NTC parameters
     *   R_ntc = R_pullup * (V / (VREF - V))
     *   T_inv = A + B * ln(R) + C * (ln(R))^3
     *   Temp_C = 1/T_inv - 273.15
     */
    (void)v;
    return 25.0f; /* Placeholder */
}

uint16_t adc_read_psu_mv(void)
{
    float v = adc_read_voltage(ADC_CH_PSU_MON);
    /* TODO: Apply voltage divider ratio
     *  e.g., 4:1 divider => multiply by 4, convert to mV
     */
    const float DIVIDER_RATIO = 4.0f;
    return (uint16_t)(v * DIVIDER_RATIO * 1000.0f);
}

const uint16_t* adc_get_buffer(void)
{
    return g_adc_buffer;
}

void adc_calibrate_channel(adc_channel_t ch, int16_t offset, float gain)
{
    if (ch >= ADC_NUM_CHANNELS) return;
    g_adc_cal[ch].offset = offset;
    g_adc_cal[ch].gain   = gain;
}

/**
 * ─── ADC ISR (ADCINT1) ──────────────────────────────────────────────
 *
 * Called when the last EOC in the SOC sequence completes.
 * Reads all results into g_adc_buffer.
 *
 * interrupt void adc_isr(void)
 * {
 *     uint16_t i;
 *     for (i = 0; i < ADC_NUM_CHANNELS; i++) {
 *         g_adc_buffer[i] = AdcResult.ADCRESULT[i];
 *     }
 *     AdcRegs.ADCINTFLGCLR.bit.ADCINT1 = 1;
 *     PieCtrlRegs.PIEACK.all |= 0x01;  // group 1 ack
 * }
 */
