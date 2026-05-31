/**
 * @file    websocket.h
 * @brief   WebSocket server for real-time telemetry streaming.
 */

#ifndef WEBSOCKET_H
#define WEBSOCKET_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Initialize WebSocket server (typically on path /ws).
 *
 * Broadcasts JSON telemetry at 10 Hz:
 *   {
 *     "v": 12.34, "i": 5.67, "p": 70.0,
 *     "mode": "CC", "status": "RUNNING",
 *     "temp_c": 45, "uptime_s": 3600
 *   }
 *
 * TODO: Implement using ESP-IDF HTTP server WebSocket support
 */
void websocket_init(void);

/**
 * @brief  Broadcast a JSON string to all connected WebSocket clients.
 * @param  json_str  Null-terminated JSON payload.
 */
void websocket_broadcast(const char* json_str);

#ifdef __cplusplus
}
#endif

#endif /* WEBSOCKET_H */
