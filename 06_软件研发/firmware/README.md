# EL-1000 Firmware — 1000W Programmable DC Electronic Load

## Overview

Dual-MCU architecture for a 1000W programmable DC electronic load.

| MCU | Role | Key Features |
|-----|------|-------------|
| **C2000 F28E12x** | Real-time control | PID @860Hz, protection @1ms, HRPWM @25kHz |
| **ESP32-S3** | Communication & UI | Wi-Fi 6 + BLE 5.0, WebSocket/REST API, 4.3" IPS LCD |

## Directory Layout

```
firmware/
├── README.md            ← This file
├── c2000/               ← C2000 F28E12x firmware (C/FreeRTOS)
│   ├── CMakeLists.txt
│   ├── main.c
│   ├── FreeRTOSConfig.h
│   ├── tasks/           ← FreeRTOS task implementations
│   ├── drivers/         ← Peripheral driver layer
│   └── control/         ← Control loop logic (PID, modes)
├── esp32/               ← ESP32-S3 firmware (ESP-IDF)
│   ├── CMakeLists.txt
│   ├── main/            ← Application code
│   └── components/      ← LVGL, protocol handlers
├── common/              ← Shared types & protocol definitions
└── docs/                ← Architecture documentation
```

## Build Instructions

### C2000
1. Open CCS Theia, import `firmware/` as a CCS project.
2. Select build target: `F28E12x`.
3. Build and flash via XDS110 debug probe.

### ESP32
1. Source ESP-IDF environment:
   ```
   . $HOME/esp/esp-idf/export.sh
   ```
2. Build:
   ```
   cd firmware/esp32
   idf.py build
   ```
3. Flash:
   ```
   idf.py -p /dev/ttyUSB0 flash monitor
   ```

## Inter-MCU Communication

UART (SCI-A on C2000 ↔ UART0 on ESP32) using a custom binary protocol defined in `common/protocol.h`.  
Baud rate: 921600. Packet format: start byte + length + command + payload + CRC.

## Real-Time Constraints

| Loop | Frequency | Deadline | MCU |
|------|-----------|----------|-----|
| PID current control | 860 Hz | 1.16 ms | C2000 |
| Protection monitor | 1 kHz | 1.00 ms | C2000 |
| HRPWM update | 25 kHz | 40 µs | C2000 (ISR) |
| UART comms | 100 Hz | 10 ms | Both |
| Display refresh | 30 Hz | 33 ms | ESP32 |
| WebSocket push | 10 Hz | 100 ms | ESP32 |
