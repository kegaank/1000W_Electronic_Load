/**
 * @file    gpio.h
 * @brief   GPIO initialization for EL-1000 C2000 F28E12x.
 */

#ifndef GPIO_H
#define GPIO_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── GPIO Pin Assignments ─────────────────────────────────────────── */
/* These must be verified against the EL-1000 schematic. */

#define GPIO_LED_STATUS       0   /**< Status LED (green) */
#define GPIO_LED_FAULT       1   /**< Fault LED (red) */
#define GPIO_LED_WIFI        2   /**< Wi-Fi status LED (blue) */
#define GPIO_RELAY_ON        3   /**< Load relay control (active high) */
#define GPIO_FAN_PWM         4   /**< Fan speed control (PWM, 25 kHz) */
#define GPIO_ALERT_OUT       5   /**< External alert/buzzer */
#define GPIO_NTC_PWR_EN      6   /**< NTC bias voltage enable */

/* GPIO muxed to peripherals (configured by respective driver) */
/* GPIO28/29: SCI-A (SCIRXDA, SCITXDA) — configured in uart.c */
/* GPIO0-3:   EPWM1A/B, EPWM2A/B — configured in hrpwm.c */

/**
 * @brief  Initialize all GPIO pins.
 *
 * Sets direction, pull-up/pull-down, and default output state for
 * all digital I/O used in the system.
 *
 * TODO: Set each GPIO's direction (GPADIR, GPBDIR)
 * TODO: Configure pull-up/down (GPAPUD, GPBPUD)
 * TODO: Configure qualification (GPACTRL, GPBCTRL)
 * TODO: Set default output states (GPASET, GPACLEAR)
 * TODO: MUX peripheral pins to correct function (GPAMUX, GPBMUX)
 */
void gpio_init(void);

/**
 * @brief  Set a GPIO output pin high.
 * @param  pin  GPIO pin number.
 */
void gpio_set(uint16_t pin);

/**
 * @brief  Clear a GPIO output pin low.
 * @param  pin  GPIO pin number.
 */
void gpio_clear(uint16_t pin);

/**
 * @brief  Toggle a GPIO output pin.
 * @param  pin  GPIO pin number.
 */
void gpio_toggle(uint16_t pin);

/**
 * @brief  Read a GPIO input pin.
 * @param  pin  GPIO pin number.
 * @return Current pin state (0 or 1).
 */
bool gpio_read(uint16_t pin);

#ifdef __cplusplus
}
#endif

#endif /* GPIO_H */
