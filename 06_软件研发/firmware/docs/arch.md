# EL-1000 Firmware Architecture

## 1. System Overview

```
┌──────────────────────────────────────────────────┐
│                   ESP32-S3                        │
│  ┌──────────┐  ┌───────────┐  ┌───────────────┐  │
│  │ WebServer │  │ WebSocket │  │   LVGL UI     │  │
│  │ (REST)    │  │ (realtime)│  │   (4.3" LCD)  │  │
│  └─────┬────┘  └─────┬─────┘  └───────┬───────┘  │
│        │              │                │          │
│  ┌─────┴──────────────┴────────────────┴───────┐  │
│  │            App Message Queue                 │  │
│  └────────────────────┬────────────────────────┘  │
│                       │ UART (921600 baud)         │
├───────────────────────┼──────────────────────────┤ │
│                 ┌─────┴──────┐                     │
│                 │ UART ISR   │                     │
│                 │ (SCI-A)    │                     │
│                 └─────┬──────┘                     │
│                       │                            │
│  ┌────────────────────┼────────────────────────┐  │
│  │            C2000 F28E12x                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ PID Task │  │Protection│  │  Comm    │  │  │
│  │  │ @860Hz   │  │ @1ms     │  │  Task    │  │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  │  │
│  │       │              │             │         │  │
│  │  ┌────┴──────────────┴─────────────┴──────┐  │  │
│  │  │         FreeRTOS Scheduler             │  │  │
│  │  └───────────────────┬────────────────────┘  │  │
│  │                      │                        │  │
│  │  ┌───────────────────┴────────────────────┐  │  │
│  │  │   HAL/Driver Layer (HRPWM, ADC, CMPSS) │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

## 2. Task Map (C2000 — FreeRTOS)

| Task | Priority | Period | Stack | Description |
|------|----------|--------|-------|-------------|
| `pid_task` | 5 (highest) | 1.16 ms (860 Hz) | 512 | PID computation, DAC/HRPWM update |
| `protection_task` | 4 | 1 ms | 256 | OVP, OCP, OTP, OPP checks |
| `comm_task` | 3 | 10 ms (poll) | 512 | UART framing, command dispatch |
| `housekeeping_task` | 2 | 100 ms | 256 | ADC avg, status LED, debug log |
| `idle_task` | 0 | — | 128 | WFI sleep |

### ISR priorities
- HRPWM update (ePWM1): ISR @25 kHz — highest
- ADC EOC (end-of-conversion): ISR @860 Hz
- UART RX (SCI-A): ISR on byte received

## 3. Task Map (ESP32 — FreeRTOS)

| Task | Core | Priority | Description |
|------|------|----------|-------------|
| `uart_rx` | 0 | 10 | UART byte reception & framing |
| `ws_server` | 1 | 5 | WebSocket broadcast @10 Hz |
| `http_server` | 1 | 4 | REST API request handler |
| `display_tick` | 1 | 3 | LVGL timer tick & refresh @30 Hz |
| `encoder_scan` | 0 | 2 | Rotary encoder debounce & events |
| `wifi_mgr` | 0 | 1 | Wi-Fi reconnect, AP scan |

## 4. Data Flow

### Control path (fast, C2000 only)
```
ADC (13ch) → PID task → Duty cycle → HRPWM → MOSFET gate
       ↑                     |
       └── Protection task ──┘  (trips output on fault)
```

### Telemetry path (slow, C2000 → ESP32)
```
Housekeeping task → Ring buffer → Comm task → UART → ESP32
                                                       ↓
                                             WebSocket / LVGL / REST
```

### Command path (ESP32 → C2000)
```
UI / API / WebSocket → Comm task (ESP32) → UART → Comm task (C2000)
                                                       ↓
                                              Mode switch / Setpoint
```

## 5. Protection Strategy

Protection is **hardware-backed** with CMPSS comparators on the C2000 for
the fastest trip times, and **software-monitored** by the protection task
for configurable thresholds and hysteresis.

| Protection | Hardware | Software | Action |
|-----------|----------|----------|--------|
| OVP | CMPSS1 (V > threshold) | ADC check @1ms | PWM trip + GPIO shutdown |
| OCP | CMPSS2 (I > threshold) | ADC check @1ms | PWM trip + GPIO shutdown |
| OTP | — | NTC ADC @100ms | Foldback then shutdown |
| OPP | — | V*I compute @1ms | Foldback then shutdown |
| Reverse V | External comparator | — | MOSFET body diode blocks |

## 6. HRPWM Configuration

- **PWM frequency**: 25 kHz (Tperiod = 40 µs)
- **HRPWM resolution**: ~150 ps (MEP step)
- **Dead-band**: 200 ns (complementary PWM for synchronous rectification)
- **Trip zone**: TZ1 (CMPSS1), TZ2 (CMPSS2), TZ3 (software force)

## 7. UART Protocol

Binary frame-based protocol (see `common/protocol.h`). Frame:
```
[SYNC0: 0xAA] [SYNC1: 0x55] [LEN] [CMD] [PAYLOAD..] [CRC16-LO] [CRC16-HI]
```

ESP32 is bus master — initiates all transactions. C2000 responds within 1 ms.
