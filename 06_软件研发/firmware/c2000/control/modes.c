/**
 * @file    modes.c
 * @brief   Operating mode management implementation.
 */

#include "modes.h"
#include <string.h>

/* ─── Global state ─────────────────────────────────────────────────── */
modes_ctrl_t g_modes;

/* ─── Hardware limits ──────────────────────────────────────────────── */
#define MAX_POWER_W     1000.0f
#define MAX_CURRENT_A   110.0f
#define MAX_VOLTAGE_V   150.0f

void modes_init(modes_ctrl_t* m)
{
    memset(m, 0, sizeof(modes_ctrl_t));
    m->active_mode      = MODE_CC;
    m->output_enabled   = false;
    m->max_power_watts  = MAX_POWER_W;
    m->max_current_amps = MAX_CURRENT_A;
    m->max_voltage_volts = MAX_VOLTAGE_V;

    current_loop_init(&g_current_loop);
    voltage_loop_init(&g_voltage_loop);
}

void modes_switch(modes_ctrl_t* m, el1000_mode_t mode, const el1000_setpoints_t* sp)
{
    if (mode >= MODE_COUNT) return;

    /* Stop current output gracefully */
    current_loop_stop(&g_current_loop);
    voltage_loop_stop(&g_voltage_loop);

    m->active_mode          = mode;
    m->setpoints            = *sp;
    m->mode_change_pending  = true;

    /* Configure the target mode */
    switch (mode) {
        case MODE_CC:
            current_loop_set_target(&g_current_loop, sp->cc_setpoint.setpoint);
            break;

        case MODE_CV:
            voltage_loop_set_target(&g_voltage_loop, sp->cv_setpoint.setpoint);
            break;

        case MODE_CR: {
            /* CR mode: compute current demand from V / R
             * The outer loop regulates R by adjusting current demand.
             * For now, we convert to CC equivalent at the start:
             *   I_demand = V_measured / R_setpoint
             * TODO: Implement true resistance-based PID
             */
            float r = sp->cr_setpoint.setpoint;
            if (r > 0.0f) {
                /* Placeholder — actual regulation is done in modes_run */
            }
            break;
        }

        case MODE_CW: {
            /* CW mode: compute current from P / V
             * TODO: Implement true power-based PID (outer loop)
             */
            break;
        }

        case MODE_DYN:
        case MODE_BAT:
            /* TODO: Implement dynamic load and battery test modes */
            break;

        default:
            break;
    }

    m->mode_change_pending = false;
}

void modes_set_output(modes_ctrl_t* m, bool en)
{
    if (en && !m->output_enabled) {
        /* TODO: Close load relay (GPIO_RELAY_ON = 1) */
        /* TODO: Enable PWM outputs (hrpwm_trip_recover() if tripped) */
        m->output_enabled = true;
    } else if (!en && m->output_enabled) {
        /* TODO: Open load relay (GPIO_RELAY_ON = 0) */
        /* TODO: Force HRPWM to 0% duty */
        /* TODO: hrpwm_force_shutdown() for safety */
        current_loop_stop(&g_current_loop);
        voltage_loop_stop(&g_voltage_loop);
        m->output_enabled = false;
    }
}

float modes_run(modes_ctrl_t* m, float measured_v, float measured_a)
{
    if (!m->output_enabled) {
        return 0.0f;
    }

    float duty = 0.0f;

    switch (m->active_mode) {
        case MODE_CC:
            duty = current_loop_run(&g_current_loop, measured_a);
            break;

        case MODE_CV: {
            float i_demand = voltage_loop_run(&g_voltage_loop, measured_v);
            current_loop_set_target(&g_current_loop, i_demand);
            duty = current_loop_run(&g_current_loop, measured_a);
            break;
        }

        case MODE_CR: {
            /* CR mode: I = V / R
             * Use voltage PID to produce current demand proportional to error
             * between desired R and actual R = V / I.
             */
            float r_target = m->setpoints.cr_setpoint.setpoint;
            if (r_target > 0.0f && measured_a > 0.001f) {
                float actual_r = measured_v / measured_a;
                float r_error = r_target - actual_r;
                /* TODO: Proper CR PID loop — for now proportional only */
                float i_adjust = r_error * 0.1f;
                float i_target = (measured_v / r_target) + i_adjust;
                current_loop_set_target(&g_current_loop, i_target);
            }
            duty = current_loop_run(&g_current_loop, measured_a);
            break;
        }

        case MODE_CW: {
            /* CW mode: I = P / V
             * TODO: Proper power PID loop
             */
            float p_target = m->setpoints.cw_setpoint.setpoint;
            if (p_target > 0.0f && measured_v > 0.5f) {
                float i_target = p_target / measured_v;
                current_loop_set_target(&g_current_loop, i_target);
            }
            duty = current_loop_run(&g_current_loop, measured_a);
            break;
        }

        case MODE_DYN:
            /* TODO: Dynamic load — toggle between two setpoints at transient_hz */
            break;

        case MODE_BAT:
            /* TODO: Battery discharge — constant current until cutoff voltage */
            break;

        default:
            break;
    }

    /* Update computed values */
    m->computed_power      = measured_v * measured_a;
    if (measured_a > 0.001f) {
        m->computed_resistance = measured_v / measured_a;
    } else {
        m->computed_resistance = 999999.0f; /* Open circuit */
    }

    return duty;
}

const char* modes_get_name(const modes_ctrl_t* m)
{
    return el1000_mode_str(m->active_mode);
}

float modes_get_power(const modes_ctrl_t* m)
{
    return m->computed_power;
}
