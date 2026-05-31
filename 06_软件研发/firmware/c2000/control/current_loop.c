/**
 * @file    current_loop.c
 * @brief   Current control loop implementation.
 */

#include "current_loop.h"
#include "pid.h"

/* ─── Global state ─────────────────────────────────────────────────── */
current_loop_t g_current_loop;

/* ─── Defaults ─────────────────────────────────────────────────────── */
#define MAX_CURRENT_A     110.0f   /* 110 A = ~10% above 1000W/10V */
#define MIN_DUTY          0.02f    /* 2% minimum duty for conduction */
#define SOFT_START_ITERS  100      /* ~116 ms at 860 Hz */

void current_loop_init(current_loop_t* cl)
{
    cl->target_current     = 0.0f;
    cl->measured_current   = 0.0f;
    cl->duty_output        = 0.0f;
    cl->soft_start_active  = false;
    cl->soft_start_target  = 0.0f;
    cl->soft_start_current = 0.0f;
    cl->soft_start_step    = 0.0f;
    cl->soft_start_iters   = SOFT_START_ITERS;
    cl->max_current        = MAX_CURRENT_A;
    cl->min_duty           = MIN_DUTY;

    pid_init(&g_pid_state);
}

void current_loop_set_target(current_loop_t* cl, float amps)
{
    if (amps > cl->max_current) {
        amps = cl->max_current;
    }

    if (amps <= 0.0f) {
        current_loop_stop(cl);
        return;
    }

    cl->soft_start_target  = amps;
    cl->soft_start_current = 0.0f;
    cl->soft_start_step    = amps / (float)cl->soft_start_iters;
    cl->soft_start_active  = true;

    /* Reset PID to prevent integral windup from large step */
    pid_reset(&g_pid_state);
}

float current_loop_run(current_loop_t* cl, float measured_a)
{
    cl->measured_current = measured_a;

    float effective_target = cl->target_current;

    if (cl->soft_start_active) {
        cl->soft_start_current += cl->soft_start_step;
        if (cl->soft_start_current >= cl->soft_start_target) {
            cl->soft_start_current  = cl->soft_start_target;
            cl->soft_start_active   = false;
        }
        effective_target = cl->soft_start_current;
    }

    cl->duty_output = pid_update(&g_pid_state, effective_target, measured_a);

    /* Enforce minimum duty if output is non-zero */
    if (cl->duty_output > 0.0f && cl->duty_output < cl->min_duty) {
        cl->duty_output = cl->min_duty;
    }

    /* TODO: Write duty to HRPWM:
     *   uint16_t cmp_val = (uint16_t)(cl->duty_output * hrpwm_get_period());
     *   hrpwm_set_duty_epwm1(cmp_val);
     */

    return cl->duty_output;
}

void current_loop_stop(current_loop_t* cl)
{
    cl->target_current    = 0.0f;
    cl->soft_start_active = false;
    cl->soft_start_target = 0.0f;
    cl->soft_start_current = 0.0f;
    cl->duty_output       = 0.0f;
    pid_reset(&g_pid_state);

    /* TODO: Force HRPWM to 0% duty:
     *   hrpwm_set_duty_epwm1(0);
     */
}

bool current_loop_is_active(const current_loop_t* cl)
{
    return (cl->target_current > 0.0f) || cl->soft_start_active;
}
