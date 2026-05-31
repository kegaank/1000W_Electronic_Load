/**
 * @file    el1000_types.h
 * @brief   Shared data types for EL-1000 electronic load.
 *          Used by both C2000 and ESP32 firmware.
 */

#ifndef EL1000_TYPES_H
#define EL1000_TYPES_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ─── Operating Modes ─────────────────────────────────────────────── */

typedef enum {
    MODE_CC = 0,    /**< Constant Current */
    MODE_CV,        /**< Constant Voltage */
    MODE_CR,        /**< Constant Resistance */
    MODE_CW,        /**< Constant Power */
    MODE_DYN,       /**< Dynamic load (transient) */
    MODE_BAT,       /**< Battery discharge */
    MODE_COUNT
} el1000_mode_t;

/* ─── Setpoint Parameters ─────────────────────────────────────────── */

typedef struct {
    float setpoint;     /**< Primary setpoint (A, V, Ω, or W) */
    float range_max;    /**< Full-scale range for this parameter */
    float resolution;   /**< Step resolution */
} __attribute__((packed)) el1000_param_t;

typedef struct {
    el1000_mode_t  mode;            /**< Active operating mode */
    el1000_param_t cc_setpoint;     /**< Constant Current target (A) */
    el1000_param_t cv_setpoint;     /**< Constant Voltage target (V) */
    el1000_param_t cr_setpoint;     /**< Constant Resistance target (Ω) */
    el1000_param_t cw_setpoint;     /**< Constant Power target (W) */
    uint32_t       transient_hz;    /**< Dynamic mode frequency (Hz) */
    float          transient_duty;  /**< Dynamic mode duty cycle (0.0–1.0) */
    float          transient_lo;    /**< Dynamic low current/voltage */
    float          transient_hi;    /**< Dynamic high current/voltage */
} __attribute__((packed)) el1000_setpoints_t;

/* ─── Telemetry (realtime readings) ────────────────────────────────── */

typedef struct {
    float    voltage;           /**< Measured voltage (V) */
    float    current;           /**< Measured current (A) */
    float    power;             /**< Computed power (W) */
    float    resistance;        /**< Computed load resistance (Ω) */
    float    vref_adc;          /**< Raw ADC count for Vref channel */
    float    iref_adc;          /**< Raw ADC count for Iref channel */
    uint16_t vbatt_mv;          /**< Battery voltage (mV) for battery test */
    uint16_t ibatt_ma;          /**< Battery current (mA) */
    int16_t  temperature_c;     /**< Heatsink temperature (°C) */
    uint32_t timestamp_us;      /**< Microsecond timestamp of sample */
} __attribute__((packed)) el1000_telemetry_t;

/* ─── System Status & Protection ───────────────────────────────────── */

typedef enum {
    PROT_NONE        = 0x00,
    PROT_OVP         = 0x01,  /**< Over-voltage protection */
    PROT_OCP         = 0x02,  /**< Over-current protection */
    PROT_OPP         = 0x04,  /**< Over-power protection */
    PROT_OTP         = 0x08,  /**< Over-temperature protection */
    PROT_REV_V       = 0x10,  /**< Reverse voltage protection */
    PROT_FAULT       = 0x20,  /**< General hardware fault */
    PROT_COMMS_LOST  = 0x40,  /**< UART communication lost */
} el1000_prot_flags_t;

typedef enum {
    STATUS_IDLE      = 0,
    STATUS_RUNNING   = 1,
    STATUS_FAULT     = 2,
    STATUS_CAL       = 3,   /**< Calibration mode */
} el1000_sys_status_t;

typedef struct {
    el1000_sys_status_t  status;
    el1000_prot_flags_t  protection_flags;
    uint32_t             uptime_sec;
    uint16_t             psu_voltage_mv;   /**< Internal PSU rail */
    uint8_t              fault_reason;     /**< Extended fault code */
    uint8_t              cal_in_progress;  /**< 0=no, 1=yes */
} __attribute__((packed)) el1000_sys_status_t;

/* ─── Calibration Data ─────────────────────────────────────────────── */

typedef struct {
    float v_offset;     /**< Voltage ADC offset */
    float v_gain;       /**< Voltage ADC gain */
    float i_offset;     /**< Current ADC offset */
    float i_gain;       /**< Current ADC gain */
    uint8_t cal_valid;  /**< 0 = invalid, 1 = valid */
    uint32_t cal_date;  /**< Unix timestamp of last cal */
} __attribute__((packed)) el1000_calibration_t;

/* ─── Enum ↔ String helpers ────────────────────────────────────────── */

static inline const char* el1000_mode_str(el1000_mode_t m) {
    static const char* names[] = {"CC","CV","CR","CW","DYN","BAT"};
    return (m < MODE_COUNT) ? names[m] : "???";
}

static inline const char* el1000_status_str(el1000_sys_status_t s) {
    static const char* names[] = {"IDLE","RUNNING","FAULT","CAL"};
    return (s < 4) ? names[s] : "???";
}

#ifdef __cplusplus
}
#endif

#endif /* EL1000_TYPES_H */
