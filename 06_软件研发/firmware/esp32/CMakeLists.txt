# ============================================================================
# CMakeLists.txt — ESP32-S3 firmware for EL-1000
# ============================================================================
cmake_minimum_required(VERSION 3.16)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)

project(el1000_esp32)

# ─── Component directories ──────────────────────────────────────────
set(EXTRA_COMPONENT_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}/components/lvgl
    ${CMAKE_CURRENT_SOURCE_DIR}/components/protocol
)
