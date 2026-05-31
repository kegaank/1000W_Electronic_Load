/**
 * @file    FreeRTOSConfig.h
 * @brief   FreeRTOS configuration for C2000 F28E12x.
 *          Configured for tight real-time constraints.
 */

#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/* ─── C2000 specifics ─────────────────────────────────────────────── */
#define configUSE_PREEMPTION              1
#define configUSE_PORT_OPTIMISED_TASK_SELECTION 1
#define configCPU_CLOCK_HZ                ((unsigned long)120000000) /* 120 MHz */
#define configTICK_RATE_HZ                ((TickType_t)1000)
#define configMINIMAL_STACK_SIZE          ((unsigned short)128)
#define configTOTAL_HEAP_SIZE             ((size_t)(32 * 1024))  /* 32 KB heap */

/* ─── Task Priorities ──────────────────────────────────────────────── */
#define PID_TASK_PRIORITY                 (configMAX_PRIORITIES - 1)  /* Highest */
#define PROTECTION_TASK_PRIORITY          (configMAX_PRIORITIES - 2)
#define COMM_TASK_PRIORITY                (configMAX_PRIORITIES - 3)
#define HOUSEKEEPING_TASK_PRIORITY        (configMAX_PRIORITIES - 4)

/* ─── Feature enables ──────────────────────────────────────────────── */
#define configUSE_IDLE_HOOK               0
#define configUSE_TICK_HOOK               1
#define configUSE_TIMERS                  1
#define configUSE_CO_ROUTINES             0
#define configUSE_MUTEXES                 1
#define configUSE_RECURSIVE_MUTEXES       1
#define configUSE_COUNTING_SEMAPHORES     1
#define configUSE_QUEUE_SETS              0
#define configUSE_TASK_NOTIFICATIONS      1
#define configSUPPORT_DYNAMIC_ALLOCATION  1
#define configSUPPORT_STATIC_ALLOCATION   0

/* ─── Assert / Stack Overflow ──────────────────────────────────────── */
#define configCHECK_FOR_STACK_OVERFLOW    2
#define configASSERT(x)                   if (!(x)) { taskDISABLE_INTERRUPTS(); for(;;); }

/* ─── Interrupt nesting ────────────────────────────────────────────── */
#define configKERNEL_INTERRUPT_PRIORITY   1
#define configMAX_SYSCALL_INTERRUPT_PRIORITY 4
#define configMAX_API_CALL_INTERRUPT_PRIORITY 4

/* ─── Queues & semaphore lengths ───────────────────────────────────── */
#define QUEUE_LENGTH_TELEMETRY            4
#define QUEUE_LENGTH_COMMANDS             8
#define QUEUE_LENGTH_LOG                  16

/* ─── Trace / Debug ────────────────────────────────────────────────── */
#define configUSE_TRACE_FACILITY          1
#define configGENERATE_RUN_TIME_STATS     0
#define configUSE_STATS_FORMATTING_FUNCTIONS 0

/* ─── Timer task ───────────────────────────────────────────────────── */
#define configTIMER_TASK_PRIORITY         (configMAX_PRIORITIES - 5)
#define configTIMER_QUEUE_LENGTH          5
#define configTIMER_TASK_STACK_DEPTH      (configMINIMAL_STACK_SIZE)

/* ─── Include the FreeRTOS API headers ────────────────────────────── */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include "timers.h"

#endif /* FREERTOS_CONFIG_H */
