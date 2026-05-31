/**
 * @file    webserver.c
 * @brief   REST API server implementation.
 */

#include "webserver.h"
#include "esp_log.h"

static const char *TAG = "WEBSERVER";

void webserver_init(void)
{
    /* TODO: Create ESP-IDF HTTP server handle
     *
     * httpd_handle_t server = NULL;
     * httpd_config_t config = HTTPD_DEFAULT_CONFIG();
     * config.uri_match_fn = httpd_uri_match_wildcard;
     *
     * if (httpd_start(&server, &config) == ESP_OK) {
     *     // Register URI handlers
     *     httpd_register_uri_handler(server, &uri_get_status);
     *     httpd_register_uri_handler(server, &uri_get_telemetry);
     *     httpd_register_uri_handler(server, &uri_get_config);
     *     httpd_register_uri_handler(server, &uri_put_config);
     *     httpd_register_uri_handler(server, &uri_post_output);
     * }
     */
    ESP_LOGI(TAG, "REST API server started on port 80");
}
