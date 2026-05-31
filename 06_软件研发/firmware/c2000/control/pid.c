/**
 * @file    pid.c
 * @brief   PID controller implementation.
 */

#include "pid.h"

/* ─── Global PID state ─────────────────────────────────────────────── */
pid_ctrl_t g_pid_state;

void pid_init(pid_ctrl_t* pid)
{
    pid->kp        = 0.5f;
    pid->ki        = 10.0f;
    pid->kd        = 0.001f;
    pid->dt        = 1.0f / 860.0f;   /* ~0.001163 s */
    pid->max_output  = 0.95f;
    pid->min_output  = 0.0f;
    pid->max_integral = 0.95f;   /* 30A稳态duty~0.88, 需≥0.88 (per pid_sim.py) */
    pid->min_integral = -0.95f;

    pid->integral       = 0.0f;
    pid->prev_error     = 0.0f;
    pid->prev_output    = 0.0f;
    pid->prev_measurement = 0.0f;

    pid->enabled    = true;
    pid->run_count  = 0;
}

void pid_reset(pid_ctrl_t* pid)
{
    pid->integral        = 0.0f;
    pid->prev_error      = 0.0f;
    pid->prev_output     = 0.0f;
    pid->prev_measurement = 0.0f;
    pid->run_count       = 0;
}

void pid_set_gains(pid_ctrl_t* pid, float kp, float ki, float kd)
{
    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
}

void pid_set_limits(pid_ctrl_t* pid, float min, float max)
{
    pid->min_output = min;
    pid->max_output = max;
}

float pid_update(pid_ctrl_t* pid, float setpoint, float measurement)
{
    if (!pid->enabled) {
        return pid->prev_output;
    }

    float error = setpoint - measurement;

    /* ─── Proportional ─────────────────────────────────────────────── */
    float p_term = pid->kp * error;

    /* ─── Integral (trapezoidal approximation) ──────────────────────── */
    pid->integral += pid->ki * error * pid->dt;
    /* Clamp integral to prevent windup */
    if (pid->integral > pid->max_integral) pid->integral = pid->max_integral;
    if (pid->integral < pid->min_integral) pid->integral = pid->min_integral;
    float i_term = pid->integral;

    /* ─── Derivative (on measurement — avoids derivative kick) ──────── */
    float d_term = -pid->kd * (measurement - pid->prev_measurement) / pid->dt;

    /* ─── Sum ───────────────────────────────────────────────────────── */
    float output = p_term + i_term + d_term;

    /* ─── Clamp output ──────────────────────────────────────────────── */
    if (output > pid->max_output) output = pid->max_output;
    if (output < pid->min_output) output = pid->min_output;

    /* ─── Update state ──────────────────────────────────────────────── */
    pid->prev_error       = error;
    pid->prev_output      = output;
    pid->prev_measurement = measurement;
    pid->run_count++;

    return output;
}

/**
 * TODO: Consider adding:
 *   - Feed-forward term for faster transient response
 *   - Bumpless transfer support (when switching modes)
 *   - Scheduled gains (gain scheduling based on operating point)
 *   - Auto-tune routine (relay feedback method)
 */
