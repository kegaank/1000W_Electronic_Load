/**
 * @file    voltage_loop.c
 * @brief   Voltage control loop implementation.
 */

#include "voltage_loop.h"

/* ─── Global state ─────────────────────────────────────────────────── */
voltage_loop_t g_voltage_loop;

#define MAX_VOLTAGE_V       150.0f   /* 150 V abs max */
#define MAX_CURRENT_DEMAND  110.0f   /* Clamp current demand to HW limit */

void voltage_loop_init(voltage_loop_t* vl)
{
    vl->target_voltage     = 0.0f;
    vl->measured_voltage   = 0.0f;
    vl->current_demand     = 0.0f;
    vl->max_voltage        = MAX_VOLTAGE_V;
    vl->max_current_demand = MAX_CURRENT_DEMAND;

    /* Voltage PID tends to be slower (lower bandwidth) than current PID */
    pid_init(&vl->pid);
    vl->pid.kp = 0.2f;
    vl->pid.ki = 2.0f;
    vl->pid.kd = 0.0f;
    vl->pid.max_output = MAX_CURRENT_DEMAND;
    vl->pid.min_output = 0.0f;
    vl->pid.max_integral = 10.0f;
    vl->pid.min_integral = -10.0f;
}

void voltage_loop_set_target(voltage_loop_t* vl, float volts)
{
    if (volts > vl->max_voltage) {
        volts = vl->max_voltage;
    }
    vl->target_voltage = volts;
}

float voltage_loop_run(voltage_loop_t* vl, float measured_v)
{
    vl->measured_voltage = measured_v;

    if (vl->target_voltage <= 0.0f) {
        vl->current_demand = 0.0f;
        return 0.0f;
    }

    /* Outer voltage PID produces a current demand for the inner current loop */
    vl->current_demand = pid_update(&vl->pid, vl->target_voltage, measured_v);

    /* Clamp */
    if (vl->current_demand > vl->max_current_demand)
        vl->current_demand = vl->max_current_demand;
    if (vl->current_demand < 0.0f)
        vl->current_demand = 0.0f;

    /* TODO: Pass current_demand to inner current loop
     *   current_loop_set_target(&g_current_loop, vl->current_demand);
     */

    return vl->current_demand;
}

void voltage_loop_stop(voltage_loop_t* vl)
{
    vl->target_voltage = 0.0f;
    vl->current_demand = 0.0f;
    pid_reset(&vl->pid);
}

bool voltage_loop_is_active(const voltage_loop_t* vl)
{
    return (vl->target_voltage > 0.0f);
}
