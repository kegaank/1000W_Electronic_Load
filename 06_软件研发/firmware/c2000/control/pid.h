/**
 * @file    pid.h
 * @brief   PID controller implementation for EL-1000.
 *          Discrete-time PID with anti-windup, output clamping,
 *          and bumpless mode transfer.
 */

#ifndef PID_H
#define PID_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── PID state structure ──────────────────────────────────────────── */
typedef struct {
    /* Gains (set by configuration) */
    float kp;               /**< Proportional gain */
    float ki;               /**< Integral gain */
    float kd;               /**< Derivative gain */

    /* Tuning */
    float dt;               /**< Sample period (seconds). For 860 Hz: ~0.001163 s */
    float max_output;       /**< Maximum output clamp */
    float min_output;       /**< Minimum output clamp */
    float max_integral;     /**< Integral anti-windup limit (clamp) */
    float min_integral;

    /* Runtime state */
    float integral;         /**< Accumulated integral term */
    float prev_error;       /**< Previous error for derivative */
    float prev_output;      /**< Previous output for bumpless transfer */
    float prev_measurement; /**< Previous measurement (for "measurement derivative") */

    /* Flags */
    bool  enabled;          /**< Controller enabled */
    uint32_t run_count;     /**< Number of iterations executed */
} pid_ctrl_t;

/* ─── Global PID state (defined in pid.c) ──────────────────────────── */
extern pid_ctrl_t g_pid_state;

/* ─── Public API ───────────────────────────────────────────────────── */

/**
 * @brief  Initialize PID controller with default parameters.
 * @param  pid  Pointer to PID state structure.
 *
 * Defaults for EL-1000 current loop:
 *   dt = 1.0f / 860.0f
 *   kp = 0.5, ki = 10.0, kd = 0.001
 *   max_output = 0.95, min_output = 0.0
 *   max_integral = 0.5, min_integral = -0.5
 *
 * TODO: Tune gains through empirical testing / Ziegler-Nichols
 */
void pid_init(pid_ctrl_t* pid);

/**
 * @brief  Reset PID state (zero integral, clear derivative memory).
 * @param  pid  Pointer to PID state.
 */
void pid_reset(pid_ctrl_t* pid);

/**
 * @brief  Set PID gains at runtime.
 * @param  pid  Pointer to PID state.
 * @param  kp   Proportional gain
 * @param  ki   Integral gain
 * @param  kd   Derivative gain
 */
void pid_set_gains(pid_ctrl_t* pid, float kp, float ki, float kd);

/**
 * @brief  Set output limits (clamp).
 * @param  pid  Pointer to PID state.
 * @param  min  Minimum output value
 * @param  max  Maximum output value
 */
void pid_set_limits(pid_ctrl_t* pid, float min, float max);

/**
 * @brief  Execute one iteration of the PID controller.
 *
 * Uses the "measurement derivative" form to avoid derivative kick:
 *   error    = setpoint - measurement
 *   proportional = kp * error
 *   integral     = ki * integral * dt
 *   derivative   = -kd * (measurement - prev_measurement) / dt
 *   output   = proportional + integral + derivative
 *   output   = clamp(output, min_output, max_output)
 *
 * @param  pid         Pointer to PID state.
 * @param  setpoint    Target value (e.g., target current in A)
 * @param  measurement Measured value (e.g., actual current in A)
 * @return Controller output (duty cycle 0.0–1.0 for HRPWM)
 */
float pid_update(pid_ctrl_t* pid, float setpoint, float measurement);

#ifdef __cplusplus
}
#endif

#endif /* PID_H */
