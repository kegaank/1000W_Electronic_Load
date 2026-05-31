/**
 * @file    housekeeping_task.c
 * @brief   Low-priority housekeeping task.
 *
 * Runs at ~10 Hz. Responsibilities:
 *   - ADC oversampling / averaging for slow channels (temperature, PSU)
 *   - System status LED patterns
 *   - Debug log messages via the log queue
 *   - Fan speed control based on temperature
 *   - Periodic EEPROM/FRAM save for settings persistence
 *   - Supervisor — check if PID task is still running (watchdog)
 */

#include "FreeRTOSConfig.h"
#include "adc.h"
#include "gpio.h"
#include "modes.h"
#include "el1000_types.h"
#include <string.h>

/* ─── LED blink patterns ───────────────────────────────────────────── */
#define LED_BLINK_NORMAL    250    /* 250 ms on/off */
#define LED_BLINK_FAULT     100    /* 100 ms fast blink */
#define LED_BLINK_COMMS     500    /* 500 ms slow blink */
#define LED_BLINK_IDLE      1000   /* 1 s single pulse */

/* ─── Oversampling ─────────────────────────────────────────────────── */
#define OVERSAMPLE_COUNT    20     /* Average 20 readings at 860 Hz ~23 ms */

static struct {
    float temp_sum;
    float psu_sum;
    uint32_t sample_count;
} g_oversample;

/* ─── Task runtime stats ───────────────────────────────────────────── */
static uint32_t g_task_iterations = 0;
static uint32_t g_pid_task_watchdog = 0;

/* Forward declaration of PID task iteration counter from pid_task.c */
/* In production, the PID task would increment a shared counter */

/**
 * @brief  Housekeeping task.
 *
 * @param  pvParameters  Unused.
 */
void housekeeping_task(void *pvParameters)
{
    (void)pvParameters;
    TickType_t last_wake = xTaskGetTickCount();

    /* Initialize oversample buffer */
    memset(&g_oversample, 0, sizeof(g_oversample));

    for (;;) {
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(100));  /* 10 Hz */

        g_task_iterations++;

        /* ─── 1. Oversample slow ADC channels ─────────────────────────── */
        g_oversample.temp_sum += adc_read_temperature(ADC_CH_TEMP1);
        g_oversample.psu_sum  += (float)adc_read_psu_mv();
        g_oversample.sample_count++;

        if (g_oversample.sample_count >= OVERSAMPLE_COUNT) {
            float avg_temp = g_oversample.temp_sum / (float)OVERSAMPLE_COUNT;
            float avg_psu  = g_oversample.psu_sum / (float)OVERSAMPLE_COUNT;

            /* Update global status with averaged values */
            /* TODO: Store averaged temperature, PSU voltage */
            /* g_sys_status.psu_voltage_mv = (uint16_t)avg_psu; */

            /* Fan speed control based on temperature */
            /* TODO: Implement fan speed curve
             *   if (avg_temp < 40.0f)   fan_duty = 0.3f;   // 30%
             *   if (avg_temp > 70.0f)   fan_duty = 1.0f;   // 100%
             *   hrpwm_set_duty_epwm2((uint16_t)(fan_duty * 2400));
             */

            /* Reset */
            g_oversample.temp_sum = 0.0f;
            g_oversample.psu_sum  = 0.0f;
            g_oversample.sample_count = 0;
        }

        /* ─── 2. Status LED patterns ──────────────────────────────────── */
        if (g_sys_status.protection_flags != PROT_NONE) {
            /* Fault: fast red blink */
            gpio_toggle(GPIO_LED_FAULT);
            gpio_clear(GPIO_LED_STATUS);
        } else if (g_sys_status.status == STATUS_RUNNING) {
            /* Running: solid green */
            gpio_set(GPIO_LED_STATUS);
            gpio_clear(GPIO_LED_FAULT);
        } else if (g_sys_status.protection_flags & PROT_COMMS_LOST) {
            /* Comms lost: slow blue blink */
            gpio_toggle(GPIO_LED_WIFI);
            gpio_clear(GPIO_LED_STATUS);
        } else {
            /* Idle: slow green pulse */
            gpio_toggle(GPIO_LED_STATUS);
            gpio_clear(GPIO_LED_FAULT);
        }

        /* ─── 3. PID task watchdog ─────────────────────────────────────── */
        /* Check that g_pid_state.run_count has increased since last check.
         * If not, the PID task may be stuck.
         */
        /* TODO: Compare current run_count with stored value
         *   uint32_t current_run = g_pid_state.run_count;
         *   if (current_run == g_pid_task_watchdog) {
         *       // PID task not running — emergency shutdown
         *       hrpwm_force_shutdown();
         *       modes_set_output(&g_modes, false);
         *       g_sys_status.status = STATUS_FAULT;
         *       g_sys_status.protection_flags |= PROT_FAULT;
         *   }
         *   g_pid_task_watchdog = current_run;
         */

        /* ─── 4. Push telemetry to queue for comm_task ───────────────── */
        /* xQueueOverwrite(g_telemetry_queue, &g_telemetry); */

        /* ─── 5. Debug log (optional) ──────────────────────────────────── */
        /* char log_buf[64];
         * snprintf(log_buf, sizeof(log_buf), "V=%.2f I=%.2f T=%d",
         *          g_telemetry.voltage, g_telemetry.current,
         *          g_telemetry.temperature_c);
         * xQueueSend(g_log_queue, log_buf, 0);
         */
    }
}

/**
 * TODO:
 *   - Implement EEPROM/FRAM save for calibration and settings persistence
 *   - Add RTC timestamping for data log entries
 *   - Implement SD card logging if hardware option is added
 *   - Add self-test routine on startup
 *   - Implement debug console via secondary UART if available
 */
