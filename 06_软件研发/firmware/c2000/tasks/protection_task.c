/**
 * @file    protection_task.c
 * @brief   Protection monitoring task @ 1 ms.
 *
 * Monitors system for fault conditions and responds with appropriate
 * actions (foldback, shutdown, alert). Runs at 1 kHz, one priority
 * level below the PID task.
 *
 * Protection checks (in order of criticality):
 *   1. CMPSS hardware trip flags (instant, latched)
 *   2. OVP — Software voltage > threshold
 *   3. OCP — Software current > threshold
 *   4. OPP — Computed power > 1000 W
 *   5. OTP — Heatsink temperature > limit
 *   6. Comms — Lost communication with ESP32
 *   7. PSU — Internal rail voltage out of range
 */

#include "FreeRTOSConfig.h"
#include "adc.h"
#include "cmpss.h"
#include "hrpwm.h"
#include "gpio.h"
#include "modes.h"
#include "el1000_types.h"
#include <string.h>

/* ─── Protection thresholds ────────────────────────────────────────── */
/* TODO: Make these configurable via UART command */
#define PROT_OVP_THRESHOLD_V     150.0f   /* 150 V */
#define PROT_OCP_THRESHOLD_A     110.0f   /* 110 A */
#define PROT_OPP_THRESHOLD_W     1050.0f  /* 1050 W (50 W margin) */
#define PROT_OTP_THRESHOLD_C     90.0f    /* 90 °C heatsink */
#define PROT_OTP_FOLDBACK_C      75.0f    /* 75 °C — start power foldback */
#define PROT_OTP_HYSTERESIS_C    10.0f    /* Recovery hysteresis */
#define PROT_COMMS_TIMEOUT_MS    500      /* 500 ms no response from ESP32 */

/* ─── Protection thresholds with hysteresis ────────────────────────── */
static struct {
    float ovp_thresh_v;
    float ocp_thresh_a;
    float opp_thresh_w;
    float otp_thresh_c;
    float otp_foldback_c;
    float otp_hysteresis_c;
    float comms_timeout_ms;
} g_prot_cfg = {
    .ovp_thresh_v      = PROT_OVP_THRESHOLD_V,
    .ocp_thresh_a      = PROT_OCP_THRESHOLD_A,
    .opp_thresh_w      = PROT_OPP_THRESHOLD_W,
    .otp_thresh_c      = PROT_OTP_THRESHOLD_C,
    .otp_foldback_c    = PROT_OTP_FOLDBACK_C,
    .otp_hysteresis_c  = PROT_OTP_HYSTERESIS_C,
    .comms_timeout_ms  = PROT_COMMS_TIMEOUT_MS,
};

/* ─── Comms watchdog ───────────────────────────────────────────────── */
static TickType_t g_last_comms_tick = 0;

/**
 * @brief  Called by comm_task when a valid frame is received.
 *         Resets the comms watchdog timer.
 */
void protection_comms_ping(void)
{
    g_last_comms_tick = xTaskGetTickCount();
}

/**
 * @brief  Protection monitoring task.
 *
 * @param  pvParameters  Unused.
 */
void protection_task(void *pvParameters)
{
    (void)pvParameters;
    TickType_t last_wake = xTaskGetTickCount();

    for (;;) {
        vTaskDelayUntil(&last_wake, 1);  /* 1 ms period */

        /* ─── 1. CMPSS hardware trip check ────────────────────────────── */
        if (cmpss_is_ovp_tripped() || cmpss_is_ocp_tripped()) {
            g_sys_status.protection_flags |= PROT_OVP | PROT_OCP;
            g_sys_status.status = STATUS_FAULT;
            hrpwm_force_shutdown();
            modes_set_output(&g_modes, false);
            gpio_set(GPIO_LED_FAULT);
            /* Log fault */
            continue;
        }

        /* ─── 2. Read latest telemetry ────────────────────────────────── */
        float v_load  = adc_read_voltage(ADC_CH_VLOAD);
        float i_load  = adc_read_current();
        float power   = v_load * i_load;
        float temp    = adc_read_temperature(ADC_CH_TEMP1);
        uint16_t psu  = adc_read_psu_mv();

        /* ─── 3. OVP check ──────────────────────────────────────────── */
        if (v_load > g_prot_cfg.ovp_thresh_v) {
            g_sys_status.protection_flags |= PROT_OVP;
            hrpwm_force_shutdown();
            modes_set_output(&g_modes, false);
            g_sys_status.status = STATUS_FAULT;
            goto fault_halt;
        } else {
            g_sys_status.protection_flags &= ~PROT_OVP;
        }

        /* ─── 4. OCP check ──────────────────────────────────────────── */
        if (i_load > g_prot_cfg.ocp_thresh_a) {
            g_sys_status.protection_flags |= PROT_OCP;
            hrpwm_force_shutdown();
            modes_set_output(&g_modes, false);
            g_sys_status.status = STATUS_FAULT;
            goto fault_halt;
        } else {
            g_sys_status.protection_flags &= ~PROT_OCP;
        }

        /* ─── 5. OPP check ──────────────────────────────────────────── */
        if (power > g_prot_cfg.opp_thresh_w) {
            g_sys_status.protection_flags |= PROT_OPP;
            /* Foldback or shutdown */
            hrpwm_force_shutdown();
            modes_set_output(&g_modes, false);
            g_sys_status.status = STATUS_FAULT;
            goto fault_halt;
        } else {
            g_sys_status.protection_flags &= ~PROT_OPP;
        }

        /* ─── 6. OTP check ──────────────────────────────────────────── */
        if (temp > g_prot_cfg.otp_thresh_c) {
            g_sys_status.protection_flags |= PROT_OTP;
            hrpwm_force_shutdown();
            modes_set_output(&g_modes, false);
            g_sys_status.status = STATUS_FAULT;
            goto fault_halt;
        } else if (temp > g_prot_cfg.otp_foldback_c) {
            /* TODO: Implement power foldback — linearly reduce max power
             *       as temperature exceeds foldback threshold
             */
            g_sys_status.protection_flags |= PROT_OTP;
        } else if (temp < (g_prot_cfg.otp_foldback_c - g_prot_cfg.otp_hysteresis_c)) {
            g_sys_status.protection_flags &= ~PROT_OTP;
        }

        /* ─── 7. Comms watchdog ──────────────────────────────────────── */
        TickType_t now = xTaskGetTickCount();
        if ((now - g_last_comms_tick) > pdMS_TO_TICKS(g_prot_cfg.comms_timeout_ms)) {
            g_sys_status.protection_flags |= PROT_COMMS_LOST;
            /* Don't shut down — continue running with last known settings */
            /* But flash a warning LED pattern */
        } else {
            g_sys_status.protection_flags &= ~PROT_COMMS_LOST;
        }

        /* ─── 8. PSU monitor ─────────────────────────────────────────── */
        /* TODO: Check if internal PSU rail (e.g., 12V, 5V) is within range */
        g_sys_status.psu_voltage_mv = psu;

        /* ─── 9. Update status ────────────────────────────────────────── */
        if (g_sys_status.protection_flags == PROT_NONE &&
            g_sys_status.status == STATUS_FAULT) {
            /* All clear — return to idle */
            g_sys_status.status = STATUS_IDLE;
            gpio_clear(GPIO_LED_FAULT);
        }

        continue;

fault_halt:
        /* Stay in fault state until explicitly cleared by UART command */
        /* Do nothing — continue checking in next iteration */;
    }
}

/**
 * TODO:
 *   - Implement configurable thresholds via UART command CMD_SET_PROT_THRESH
 *   - Add foldback ramp (gradually reduce limit rather than instant shutdown)
 *   - Log fault events to EEPROM for post-mortem analysis
 *   - Add recovery auto-retry with configurable retry count
 */
