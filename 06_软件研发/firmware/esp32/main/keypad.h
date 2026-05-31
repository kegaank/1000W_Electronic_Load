/**
 * @file    keypad.h
 * @brief   Button matrix / keypad handler for front-panel controls.
 */

#ifndef KEYPAD_H
#define KEYPAD_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Keypad button identifiers.
 */
typedef enum {
    KEY_NONE   = 0,
    KEY_MODE   = 1,    /* Cycle CC/CV/CR/CW */
    KEY_SELECT = 2,    /* Confirm selection */
    KEY_UP     = 3,    /* Increment parameter */
    KEY_DOWN   = 4,    /* Decrement parameter */
    KEY_ON_OFF = 5,    /* Toggle output on/off */
    KEY_LOCK   = 6,    /* Key lock */
    KEY_PRESET = 7,    /* Load preset */
} keypad_key_t;

/**
 * @brief  Initialize the keypad matrix.
 *
 * TODO: Configure row GPIOs as outputs, column GPIOs as inputs.
 * TODO: Implement scan routine with debounce (50 ms).
 */
void keypad_init(void);

/**
 * @brief  Scan the keypad and return the pressed key.
 * @return Key identifier or KEY_NONE if no key pressed.
 *
 * TODO: Matrix scan:
 *   For each row, set output low, read column inputs.
 *   Debounce with a state machine (press, hold, release).
 */
keypad_key_t keypad_scan(void);

/**
 * @brief  Register a callback for key events.
 *         Called from the keypad scan task.
 */
typedef void (*keypad_callback_t)(keypad_key_t key, bool held);
void keypad_register_callback(keypad_callback_t cb);

/**
 * @brief  Keypad scan task (runs at 20 Hz).
 */
void keypad_task(void *pvParameters);

#ifdef __cplusplus
}
#endif

#endif /* KEYPAD_H */
