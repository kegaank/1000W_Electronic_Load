# ============================================================================
# CMakeLists.txt — C2000 F28E12x firmware build configuration
# ============================================================================
cmake_minimum_required(VERSION 3.20)

project(el1000_c2000
    VERSION 1.0.0
    DESCRIPTION "EL-1000 C2000 F28E12x Firmware"
    LANGUAGES C
)

# ─── Device selection ─────────────────────────────────────────────────
set(TARGET_DEVICE "F28E12x")
set(DEVICE_HEADER  "F28E12x_device.h")

# ─── Include directories ──────────────────────────────────────────────
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/drivers
    ${CMAKE_CURRENT_SOURCE_DIR}/control
    ${CMAKE_CURRENT_SOURCE_DIR}/tasks
    ${CMAKE_CURRENT_SOURCE_DIR}/../common
)

# ─── Source files ─────────────────────────────────────────────────────
set(C2000_SOURCES
    main.c
    tasks/pid_task.c
    tasks/protection_task.c
    tasks/comm_task.c
    tasks/housekeeping_task.c
    drivers/hrpwm.c
    drivers/adc.c
    drivers/cmpss.c
    drivers/uart.c
    drivers/gpio.c
    drivers/timer.c
    control/pid.c
    control/current_loop.c
    control/voltage_loop.c
    control/modes.c
)

# ─── FreeRTOS sources ────────────────────────────────────────────────
set(FREERTOS_SOURCES
    # Paths relative to your FreeRTOS port for C2000
    # ThirdParty/FreeRTOS/Source/tasks.c
    # ThirdParty/FreeRTOS/Source/queue.c
    # ThirdParty/FreeRTOS/Source/list.c
    # ThirdParty/FreeRTOS/Source/timers.c
    # ThirdParty/FreeRTOS/Source/portable/CCS/C2000/port.c
    # ThirdParty/FreeRTOS/Source/portable/MemMang/heap_4.c
)

add_executable(${PROJECT_NAME}.out
    ${C2000_SOURCES}
    ${FREERTOS_SOURCES}
)

# ─── Compiler & linker flags ─────────────────────────────────────────
target_compile_options(${PROJECT_NAME}.out PRIVATE
    --silicon_version=28
    -ml
    -g
    --opt_level=2
    --define=F28E12x
    --include_path="${DEVICE_HEADER}"
)

target_link_options(${PROJECT_NAME}.out PRIVATE
    --rts=lib rts2800_fpu32.lib
    --stack_size=0x400
    --heap_size=0x800
    # --cmd_file="F28E12x_ram_lnk.cmd"
)

# ─── Custom flash target ─────────────────────────────────────────────
add_custom_target(flash
    COMMAND ${CMAKE_COMMAND} -E echo "Flash via CCS Theia or Uniflash"
    COMMENT "Open CCS Theia and flash ${PROJECT_NAME}.out via XDS110"
)
