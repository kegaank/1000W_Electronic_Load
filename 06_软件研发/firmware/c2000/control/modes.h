/**
 * @file    modes.h
 * @brief   Operating mode management for EL-1000.
 *          Handles CC / CV / CR / CW mode selection, transitions,
 *          and dispatches to the appropriate control loop.
 */

#ifndef MODES_H
#define MODES_H

#include <stdint.h>
#include <stdbool.h>
#include "el1000_types.h"
#include "current_loop.h"
#include "voltage_loop.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Mode state ───────────────────────────────────────────────────── */
typedef struct {
    el1000_mode_t       active_mode;    /**< Currently active operating mode */
    el1000_setpoints_t  setpoints;      /**< All setpoint parameters */

    /* Computed values */
    float computed_power;       /**< V * I for power limit check */
    float computed_resistance;  /**< V / I for resistance display */

    /* Output state */
    bool  output_enabled;       /**< Load relay + PWM enabled */
    bool  mode_change_pending;  /**< True during mode transition */

    /* Cross-mode limits */
    float max_power_watts;      /**< 1000 W hardware limit */
    float max_current_amps;     /**< Hardware OCP level */
    float max_voltage_volts;    /**< Hardware OVP level */
} modes_ctrl_t;

extern modes_ctrl_t g_modes;

/**
 * @brief  Initialize mode manager.
 * @param  m     Pointer to mode manager state.
 * @param  sp    Initial setpoints (typically zero).
 */
void modes_init(modes_ctrl_t* m);

/**
 * @brief  Switch the active operating mode.
 *
 * Handles:
 *   - Stopping the current control loop
 *   - Resetting PID states for the new mode
 *   - Setting up appropriate control loop parameters
 *   - Enabling soft-start for the new mode
 *
 * @param  m     Pointer to mode manager state.
 * @param  mode  Target operating mode.
 * @param  sp    Setpoints for the new mode.
 */
void modes_switch(modes_ctrl_t* m, el1000_mode_t mode, const el1000_setpoints_t* sp);

/**
 * @brief  Enable or disable the output (load relay + PWM).
 * @param  m     Pointer to mode manager state.
 * @param  en    true = enable output, false = disable
 */
void modes_set_output(modes_ctrl_t* m, bool en);

/**
 * @brief  Execute one control loop iteration based on active mode.
 *
 * This is called by the pid_task at 860 Hz.
 *
 * @param  m             Pointer to mode manager state.
 * @param  measured_v    Latest voltage measurement.
 * @param  measured_a    Latest current measurement.
 * @return Duty cycle (0.0–1.0) for HRPWM.
 */
float modes_run(modes_ctrl_t* m, float measured_v, float measured_a);

/**
 * @brief  Get active mode as string.
 * @param  m  Pointer to mode manager state.
 * @return Static string name (e.g., "CC", "CV").
 */
const char* modes_get_name(const modes_ctrl_t* m);

/**
 * @brief  Get the current power (V * I) with protection check.
 * @param  m  Pointer to mode manager state.
 * @return Power in watts.
 */
float modes_get_power(const modes_ctrl_t* m);

#ifdef __cplusplus
}
#endif

#endif /* MODES_H */
