/**
 * @file    websocket.c
 * @brief   WebSocket server implementation.
 */

#include "websocket.h"
#include "esp_log.h"

static const char *TAG = "WEBSOCKET";

void websocket_init(void)
{
    /* TODO: Register WebSocket handler on HTTP server at /ws
     *
     * static const httpd_uri_t ws_uri = {
     *     .uri       = "/ws",
     *     .method    = HTTP_GET,
     *     .handler   = ws_handler,
     *     .user_ctx  = NULL,
     *     .is_websocket = true,
     * };
     *
     * httpd_register_uri_handler(server, &ws_uri);
     */
    ESP_LOGI(TAG, "WebSocket server ready on /ws");
}

void websocket_broadcast(const char* json_str)
{
    /* TODO: Iterate connected WebSocket clients and send
     *
     * httpd_ws_frame_t ws_pkt = {
     *     .final = true,
     *     .fragmented = false,
     *     .type = HTTPD_WS_TYPE_TEXT,
     *     .payload = (uint8_t*)json_str,
     *     .len = strlen(json_str),
     * };
     *
     * // Use httpd_ws_send_frame_async to each client
     */
    (void)json_str;
}
