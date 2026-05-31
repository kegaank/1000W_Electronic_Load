/**
 * @file    webserver.h
 * @brief   REST API server for EL-1000.
 *          Provides HTTP endpoints for controlling and monitoring the load.
 */

#ifndef WEBSERVER_H
#define WEBSERVER_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  Initialize and start the REST API server.
 *
 * Endpoints to implement (ESP-IDF HTTP server):
 *   GET  /api/v1/status       — System status
 *   GET  /api/v1/telemetry    — Latest readings
 *   GET  /api/v1/config       — Current configuration
 *   PUT  /api/v1/config       — Update setpoints
 *   POST /api/v1/output       — Enable/disable output
 *   GET  /api/v1/log          — Recent log entries
 *   GET  /api/v1/cal          — Calibration data
 *   POST /api/v1/cal          — Write calibration
 *
 * TODO: Implement using ESP-IDF HTTP server library
 */
void webserver_init(void);

#ifdef __cplusplus
}
#endif

#endif /* WEBSERVER_H */
