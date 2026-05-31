/**
 * @file    display.c
 * @brief   Display driver implementation.
 */

#include "display.h"
#include "esp_log.h"

static const char *TAG = "DISPLAY";

void display_init(void)
{
    /* TODO: Initialize SPI bus for LCD
     *
     * spi_bus_config_t bus_cfg = {
     *     .mosi_io_num     = DISPLAY_PIN_MOSI,
     *     .miso_io_num     = DISPLAY_PIN_MISO,
     *     .sclk_io_num     = DISPLAY_PIN_SCLK,
     *     .quadwp_io_num   = -1,
     *     .quadhd_io_num   = -1,
     *     .max_transfer_sz = DISP_BUF_SIZE * sizeof(uint16_t),
     * };
     *
     * esp_lcd_panel_io_handle_t io_handle = NULL;
     * esp_lcd_panel_io_spi_config_t io_cfg = {
     *     .dc_gpio_num = DISPLAY_PIN_DC,
     *     .cs_gpio_num = DISPLAY_PIN_CS,
     *     .pclk_hz     = 40 * 1000 * 1000,
     *     ...
     * };
     *
     * esp_lcd_panel_handle_t panel_handle = NULL;
     * esp_lcd_new_panel_ili9488(io_handle, &panel_cfg, &panel_handle);
     */

    /* TODO: Initialize LVGL
     *
     * lv_init();
     * // Allocate draw buffers
     * // Register display driver
     * // Create and set default screen with UI elements
     */
    ESP_LOGI(TAG, "Display initialized (4.3\" IPS, 480x272)");
}

void display_task(void *pvParameters)
{
    (void)pvParameters;
    TickType_t last_wake = xTaskGetTickCount();

    for (;;) {
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(33));  /* ~30 Hz */

        /* TODO: Call lv_timer_handler() to process LVGL tasks */
        /* lv_timer_handler(); */

        /* TODO: Update display elements with latest telemetry */
        /* lv_label_set_text_fmt(label_voltage, "%.2f V", g_telemetry.voltage); */
        /* lv_label_set_text_fmt(label_current, "%.2f A", g_telemetry.current); */
    }
}
