/**
 * @file    main.c
 * @brief   EL-1000 C2000 F28E12x firmware entry point.
 *          Initializes hardware, creates tasks, starts FreeRTOS scheduler.
 */

#include "FreeRTOSConfig.h"
#include "gpio.h"
#include "adc.h"
#include "hrpwm.h"
#include "uart.h"
#include "cmpss.h"
#include "timer.h"
#include "pid.h"
#include "modes.h"
#include "el1000_types.h"
#include "protocol.h"

/* ─── Task handles ─────────────────────────────────────────────────── */
TaskHandle_t g_pid_task_handle;
TaskHandle_t g_protection_task_handle;
TaskHandle_t g_comm_task_handle;
TaskHandle_t g_housekeeping_task_handle;

/* ─── Queues ───────────────────────────────────────────────────────── */
QueueHandle_t g_telemetry_queue;    /**< Telemetry data to ESP32 */
QueueHandle_t g_command_queue;      /**< Incoming commands from ESP32 */
QueueHandle_t g_log_queue;          /**< Log/event messages */

/* ─── Global state ─────────────────────────────────────────────────── */
el1000_setpoints_t g_setpoints;     /**< Current operating setpoints */
el1000_telemetry_t  g_telemetry;    /**< Latest telemetry sample */
el1000_sys_status_t g_sys_status;   /**< System status & flags */
el1000_calibration_t g_cal;         /**< Calibration data */

/* ─── External task functions ──────────────────────────────────────── */
extern void pid_task(void *pvParameters);
extern void protection_task(void *pvParameters);
extern void comm_task(void *pvParameters);
extern void housekeeping_task(void *pvParameters);

/**
 * @brief  Board-level initialization.
 *         Called before the scheduler starts. Configures clocks,
 *         GPIO, peripherals, and sets default operating state.
 *
 * TODO: Implement device-specific register configuration:
 *       - DeviceInit() / SysCtrl for 120 MHz SYSCLK
 *       - Disable watchdog
 *       - Configure PLL, clock dividers
 *       - Enable FPU32
 */
static void board_init(void)
{
    /* ─── Watchdog & Clock ─────────────────────────────────────────── */
    /* TODO: Disable watchdog timer (WdRegs) */
    /* TODO: InitPll(DSP28_PLLCR, DSP28_DIVSEL) for 120 MHz SYSCLK */
    /* TODO: Enable peripheral clocks (SCI-A, ADC-A/B, ePWM1-4, CMPSS) */

    /* ─── GPIO ─────────────────────────────────────────────────────── */
    gpio_init();

    /* ─── Peripherals ──────────────────────────────────────────────── */
    adc_init();       /* 13-channel sequential sampling */
    hrpwm_init();     /* 25 kHz, HRPWM enabled on ePWM1-2 */
    cmpss_init();     /* CMPSS1 (OVP), CMPSS2 (OCP) */
    uart_init();      /* SCI-A @ 921600 baud */

    /* ─── Control variables ────────────────────────────────────────── */
    pid_init(&g_pid_state);
    modes_init(&g_setpoints);

    /* Default to idle, no protection flags */
    g_sys_status.status          = STATUS_IDLE;
    g_sys_status.protection_flags = PROT_NONE;
    g_sys_status.uptime_sec      = 0;
}

/**
 * @brief  FreeRTOS tick hook — called every tick interrupt.
 *         Used for uptime tracking and watchdog servicing.
 *
 * TODO: Kick hardware watchdog if used.
 */
void vApplicationTickHook(void)
{
    static uint32_t tick_count = 0;
    tick_count++;

    /* Increment uptime every 1000 ticks (1 second at 1 kHz tick) */
    if ((tick_count % 1000) == 0) {
        g_sys_status.uptime_sec++;
    }
}

/**
 * @brief  Malloc failed hook — called if heap allocation fails.
 */
void vApplicationMallocFailedHook(void)
{
    taskDISABLE_INTERRUPTS();
    /* TODO: Set error LED pattern, halt */
    for (;;);
}

/**
 * @brief  Stack overflow hook — called when a task overflows.
 */
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName)
{
    (void)xTask;
    (void)pcTaskName;
    taskDISABLE_INTERRUPTS();
    /* TODO: Set error LED pattern, log fault */
    for (;;);
}

/**
 * @brief  Main entry point.
 *         Initializes the board, creates FreeRTOS tasks,
 *         then starts the scheduler (never returns).
 */
int main(void)
{
    /* Disable interrupts during init */
    __asm("        setc    INTM");

    board_init();

    /* Create queues */
    g_telemetry_queue = xQueueCreate(QUEUE_LENGTH_TELEMETRY, sizeof(el1000_telemetry_t));
    g_command_queue   = xQueueCreate(QUEUE_LENGTH_COMMANDS,  sizeof(proto_frame_t));
    g_log_queue       = xQueueCreate(QUEUE_LENGTH_LOG,       sizeof(char[64]));

    if (!g_telemetry_queue || !g_command_queue || !g_log_queue) {
        /* TODO: Handle queue creation failure — flash error LED */
        for (;;);
    }

    /* Create tasks */
    xTaskCreate(pid_task,           "PID",          512, NULL, PID_TASK_PRIORITY,          &g_pid_task_handle);
    xTaskCreate(protection_task,    "PROT",         256, NULL, PROTECTION_TASK_PRIORITY,   &g_protection_task_handle);
    xTaskCreate(comm_task,          "COMM",         512, NULL, COMM_TASK_PRIORITY,          &g_comm_task_handle);
    xTaskCreate(housekeeping_task, "HOUSEKEEP",    256, NULL, HOUSEKEEPING_TASK_PRIORITY,  &g_housekeeping_task_handle);

    /* Re-enable interrupts and start scheduler */
    __asm("        clrc    INTM");
    vTaskStartScheduler();

    /* Should never reach here */
    for (;;);
    return 0;
}
