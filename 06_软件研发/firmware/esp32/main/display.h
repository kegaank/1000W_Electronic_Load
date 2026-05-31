/**
 * @file    display.h
 * @brief   LCD display driver for 4.3" IPS SPI display.
 *          Uses LVGL as the graphics library.
 */

#ifndef DISPLAY_H
#define DISPLAY_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Initialize the display and LVGL.
 *
 * Configures:
 *   - SPI bus for LCD (e.g., SPI3, 40 MHz)
 *   - Display controller (ILI9488 or similar)
 *   - LVGL display buffer (double buffered)
 *   - LVGL input device (touch/encoder)
 *   - LVGL tick interface
 *
 * TODO: Use ESP-IDF LVGL port (esp_lcd_panel_io, esp_lcd_panel_xxx)
 * TODO: Create LVGL screen layouts for:
 *       - Main dashboard (V, I, P, R, mode indicator)
 *       - Settings screen (setpoints, limits)
 *       - Graphs screen (realtime V/I over time)
 *       - Calibration screen
 *       - About / status screen
 */
void display_init(void);

/**
 * @brief  Get the LVGL display refresh task handle.
 *         The task calls lv_timer_handler() at 30 Hz.
 *
 * @return Task handle (create with xTaskCreate if needed).
 */
void display_task(void *pvParameters);

#ifdef __cplusplus
}
#endif

#endif /* DISPLAY_H */
