/**
 * @file    encoder.h
 * @brief   Rotary encoder handler for parameter adjustment.
 */

#ifndef ENCODER_H
#define ENCODER_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Initialize rotary encoder (quadrature encoder input).
 *
 * Two GPIO inputs with interrupts on both edges.
 *
 * TODO: Configure ESP-IDF GPIO interrupts for encoder A/B channels.
 * TODO: Implement state machine for quadrature decoding.
 */
void encoder_init(void);

/**
 * @brief  Read accumulated encoder ticks (differential).
 * @return Signed tick count since last read.
 *
 * Positive = clockwise, negative = counter-clockwise.
 */
int32_t encoder_read_ticks(void);

/**
 * @brief  Read encoder push-button state.
 * @return true if button is pressed.
 */
bool encoder_button_pressed(void);

#ifdef __cplusplus
}
#endif

#endif /* ENCODER_H */
