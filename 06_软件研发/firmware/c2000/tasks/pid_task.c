/**
 * @file    pid_task.c
 * @brief   PID control loop task @ 860 Hz.
 *
 * This is the highest-priority task on the C2000. It reads the latest
 * ADC samples, runs the mode-specific control law, and updates the
 * HRPWM duty cycle. The task uses a precise timing delay to maintain
 * the 860 Hz loop rate. Worst-case execution must be < 1.16 ms.
 *
 * Timing budget:
 *   - ADC read:     ~20 µs
 *   - PID compute:  ~10 µs
 *   - Mode dispatch: ~5 µs
 *   - HRPWM write:  ~5 µs
 *   - Total:        ~40 µs typical, <200 µs worst case
 */

#include "FreeRTOSConfig.h"
#include "adc.h"
#include "hrpwm.h"
#include "modes.h"
#include "pid.h"
#include "el1000_types.h"
#include <stdint.h>

/* ─── Task period ──────────────────────────────────────────────────── */
#define PID_TASK_PERIOD_MS    1   /* 1 ms period, but we aim for 860 Hz */
#define PID_TASK_DELAY_TICKS  ((TickType_t)(configTICK_RATE_HZ / 860))

/**
 * @brief  PID control task.
 *
 * Synchronized to the ADC EOC interrupt via a binary semaphore
 * or direct task notification. The ADC ISR gives the semaphore
 * at 860 Hz after all 13 channels have been sampled.
 *
 * @param  pvParameters  Unused.
 *
 * Flow:
 *   1. Wait for ADC EOC notification (860 Hz)
 *   2. Read scaled voltage & current from ADC
 *   3. Run mode-specific control (modes_run)
 *   4. Write computed duty to HRPWM
 *   5. Update global telemetry struct for other tasks
 *   6. Loop
 */
void pid_task(void *pvParameters)
{
    (void)pvParameters;
    TickType_t last_wake = xTaskGetTickCount();

    /* TODO: Wait for ADC initialization to complete before starting */

    for (;;) {
        /* Synchronize to ADC EOC (860 Hz) — use binary semaphore or
         * direct task notification from ADC ISR:
         *
         *   ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
         *
         * Fallback: use vTaskDelayUntil for precise period if ISR sync
         * is not yet implemented.
         */
        vTaskDelayUntil(&last_wake, PID_TASK_DELAY_TICKS);

        /* ─── Read measurements ─────────────────────────────────────── */
        float measured_v = adc_read_voltage(ADC_CH_VLOAD);
        float measured_a = adc_read_current();
        /* TODO: Read temperature for foldback if needed */
        /* float temp = adc_read_temperature(ADC_CH_TEMP1); */

        /* ─── Run control loop ───────────────────────────────────────── */
        float duty = modes_run(&g_modes, measured_v, measured_a);

        /* TODO: Write duty to HRPWM
         *   uint16_t cmp = (uint16_t)(duty * (float)hrpwm_get_period());
         *   hrpwm_set_duty_epwm1(cmp);
         */

        /* ─── Update global telemetry ────────────────────────────────── */
        /* The housekeeping task reads this and sends to ESP32 */
        g_telemetry.voltage       = measured_v;
        g_telemetry.current       = measured_a;
        g_telemetry.power         = measured_v * measured_a;
        g_telemetry.resistance    = (measured_a > 0.001f) ? (measured_v / measured_a) : 999999.0f;
        g_telemetry.temperature_c = (int16_t)adc_read_temperature(ADC_CH_TEMP1);
        /* TODO: Add timestamp from timer_get_tbctr() */

        /* Notify other tasks of new telemetry */
        /* xQueueOverwrite(g_telemetry_queue, &g_telemetry); */
    }
}

/**
 * TODO: Consider splitting PID task into two stages:
 *   Stage 1 (ISR context): Read ADC, compute PID, update PWM
 *   Stage 2 (task context): Logging, statistics, non-critical updates
 *
 * For now, everything is in the task for simplicity.
 */
