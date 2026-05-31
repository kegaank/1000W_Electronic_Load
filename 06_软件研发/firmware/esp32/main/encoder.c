/**
 * @file    encoder.c
 * @brief   Rotary encoder implementation.
 */

#include "encoder.h"
#include "esp_log.h"

static const char *TAG = "ENCODER";
static int32_t g_encoder_ticks = 0;

void encoder_init(void)
{
    /* TODO: Configure GPIO for encoder A and B with interrupts
     *
     * gpio_config_t io_conf = {
     *     .pin_bit_mask = (1ULL << ENC_PIN_A) | (1ULL << ENC_PIN_B),
     *     .mode = GPIO_MODE_INPUT,
     *     .pull_up_en = GPIO_PULLUP_ENABLE,
     *     .intr_type = GPIO_INTR_ANYEDGE,
     * };
     * gpio_config(&io_conf);
     *
     * // Install GPIO ISR and register handler
     * gpio_install_isr_service(0);
     * gpio_isr_handler_add(ENC_PIN_A, encoder_isr, NULL);
     * gpio_isr_handler_add(ENC_PIN_B, encoder_isr, NULL);
     */
    ESP_LOGI(TAG, "Encoder initialized");
}

int32_t encoder_read_ticks(void)
{
    int32_t ticks;
    /* TODO: Atomic read */
    ticks = g_encoder_ticks;
    g_encoder_ticks = 0;
    return ticks;
}

bool encoder_button_pressed(void)
{
    /* TODO: return !gpio_get_level(ENC_PIN_BTN); */
    return false;
}

/**
 * Encoder ISR (called from GPIO ISR context).
 *
 * TODO: Quadrature state machine:
 *   static uint8_t enc_state = 0;
 *   void encoder_isr(void *arg) {
 *       uint8_t a = gpio_get_level(ENC_PIN_A);
 *       uint8_t b = gpio_get_level(ENC_PIN_B);
 *       uint8_t new_state = (a << 1) | b;
 *       static const int8_t enc_lookup[] = {0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0};
 *       g_encoder_ticks += enc_lookup[(enc_state << 2) | new_state];
 *       enc_state = new_state;
 *   }
 */
