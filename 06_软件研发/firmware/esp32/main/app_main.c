/**
 * @file    app_main.c
 * @brief   ESP32-S3 entry point for EL-1000.
 *
 * Initializes:
 *   - NVS flash storage
 *   - Wi-Fi (STA + AP modes)
 *   - UART communication with C2000
 *   - WebSocket and REST API servers
 *   - LVGL display driver
 *   - Rotary encoder and keypad
 *   - Data logging ring buffer
 *
 * Then starts FreeRTOS tasks for each subsystem.
 */

#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "uart_comms.h"
#include "webserver.h"
#include "websocket.h"
#include "display.h"
#include "encoder.h"
#include "keypad.h"
#include "wifi.h"
#include "data_log.h"

static const char *TAG = "EL1000_MAIN";

void app_main(void)
{
    ESP_LOGI(TAG, "EL-1000 ESP32-S3 firmware starting...");

    /* ─── Initialize NVS ───────────────────────────────────────────── */
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    /* ─── Initialize subsystems ────────────────────────────────────── */
    wifi_init();            /* Wi-Fi manager */
    uart_comms_init();      /* UART to C2000 */
    webserver_init();       /* REST API */
    websocket_init();       /* WebSocket real-time data */
    display_init();         /* LVGL + 4.3" IPS LCD */
    encoder_init();         /* Rotary encoder */
    keypad_init();          /* Button matrix */
    data_log_init();        /* Ring buffer logging */

    ESP_LOGI(TAG, "All subsystems initialized. System ready.");
    ESP_LOGI(TAG, "Connect via Web UI at http://el1000.local/");
}

/**
 * TODO:
 *   - Implement OTA firmware update via WebSocket
 *   - Add mDNS responder for "el1000.local" discovery
 *   - Add MQTT bridge for home automation integration
 *   - Implement SCPI command parser for lab equipment interoperability
 */
