/**
 * @file    current_loop.h
 * @brief   Current control mode logic for EL-1000.
 *
 * Wraps the PID controller with current-specific configuration:
 *   - Setpoint: target current (amperes)
 *   - Feedback: ADC current reading
 *   - Output: duty cycle fed to HRPWM
 *   - Soft-start ramp on mode entry
 */

#ifndef CURRENT_LOOP_H
#define CURRENT_LOOP_H

#include <stdint.h>
#include <stdbool.h>
#include "pid.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Current loop state ──────────────────────────────────────────── */
typedef struct {
    float target_current;       /**< Target current setpoint (A) */
    float measured_current;     /**< Latest current feedback (A) */
    float duty_output;          /**< Output duty cycle to HRPWM (0.0–1.0) */

    /* Soft-start */
    bool  soft_start_active;    /**< Ramping up after mode entry */
    float soft_start_target;    /**< Final target during ramp */
    float soft_start_current;   /**< Current ramp level */
    float soft_start_step;      /**< Per-iteration step size */
    uint32_t soft_start_iters;  /**< Number of ramp iterations planned */

    /* Limits */
    float max_current;          /**< Hardware limit (A) */
    float min_duty;             /**< Minimum duty to maintain conduction */
} current_loop_t;

extern current_loop_t g_current_loop;

/**
 * @brief  Initialize current control loop.
 * @param  cl  Pointer to current loop state.
 */
void current_loop_init(current_loop_t* cl);

/**
 * @brief  Set the target current.
 * @param  cl     Pointer to current loop state.
 * @param  amps   Target current in amperes.
 *
 * Clamps to [0, max_current] and initiates soft-start if output was off.
 */
void current_loop_set_target(current_loop_t* cl, float amps);

/**
 * @brief  Execute one iteration of the current control loop.
 *
 * Computes PID update, applies soft-start if active, outputs duty cycle.
 *
 * @param  cl          Pointer to current loop state.
 * @param  measured_a  Measured current in amperes.
 * @return Duty cycle to feed to HRPWM (0.0–1.0).
 */
float current_loop_run(current_loop_t* cl, float measured_a);

/**
 * @brief  Stop the current loop (output zero duty, reset integral).
 * @param  cl  Pointer to current loop state.
 */
void current_loop_stop(current_loop_t* cl);

/**
 * @brief  Check if current loop is regulating (enabled and running).
 * @param  cl  Pointer to current loop state.
 * @return true if active.
 */
bool current_loop_is_active(const current_loop_t* cl);

#ifdef __cplusplus
}
#endif

#endif /* CURRENT_LOOP_H */
