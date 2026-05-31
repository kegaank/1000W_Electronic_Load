/**
 * @file    voltage_loop.h
 * @brief   Voltage control mode logic for EL-1000.
 *
 * In CV mode, the load regulates the input voltage to a setpoint.
 * The voltage loop produces a current demand that feeds into the
 * inner current loop (cascaded control).
 */

#ifndef VOLTAGE_LOOP_H
#define VOLTAGE_LOOP_H

#include <stdint.h>
#include <stdbool.h>
#include "pid.h"

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Voltage loop state ───────────────────────────────────────────── */
typedef struct {
    float target_voltage;       /**< Target voltage setpoint (V) */
    float measured_voltage;     /**< Latest voltage feedback (V) */
    float current_demand;       /**< Output: current demand for inner loop (A) */

    /* Voltage PID (outer loop in cascade) */
    pid_ctrl_t pid;             /**< Voltage PID instance */

    /* Limits */
    float max_voltage;          /**< Hardware voltage limit (V) */
    float max_current_demand;   /**< Clamp for current demand (A) */
} voltage_loop_t;

extern voltage_loop_t g_voltage_loop;

/**
 * @brief  Initialize voltage control loop.
 * @param  vl  Pointer to voltage loop state.
 */
void voltage_loop_init(voltage_loop_t* vl);

/**
 * @brief  Set the target voltage.
 * @param  vl      Pointer to voltage loop state.
 * @param  volts   Target voltage in volts.
 */
void voltage_loop_set_target(voltage_loop_t* vl, float volts);

/**
 * @brief  Execute one iteration of the voltage control loop.
 *
 * Outputs a current demand that is fed to the inner current loop.
 *
 * @param  vl          Pointer to voltage loop state.
 * @param  measured_v  Measured voltage in volts.
 * @return Current demand in amperes (for inner current loop).
 */
float voltage_loop_run(voltage_loop_t* vl, float measured_v);

/**
 * @brief  Stop the voltage loop.
 * @param  vl  Pointer to voltage loop state.
 */
void voltage_loop_stop(voltage_loop_t* vl);

/**
 * @brief  Check if voltage loop is active.
 * @param  vl  Pointer to voltage loop state.
 * @return true if active.
 */
bool voltage_loop_is_active(const voltage_loop_t* vl);

#ifdef __cplusplus
}
#endif

#endif /* VOLTAGE_LOOP_H */
