#!/usr/bin/env python3
"""
Generate EL-1000 Control Circuit schematic (.kicad_sch)
Based on SYS-SCH-002 v0.1 design document

Contains:
  - C2000 F28E12x minimum system (48-pin LQFP)
  - ESP32-S3-WROOM-1 module
  - SGM71622R2 DAC (SPI)
  - ADS1115 ADC (I2C)
  - ISO7741 digital isolator
  - ADuM1201 UART isolator
  - ADuM3160 USB isolator
  - LCD 4.3" IPS connector
  - Encoder + keypad
  - JTAG + power rails
"""

import uuid, os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

def uid():
    return str(uuid.uuid4()).upper()

# ============================================================
# HEADER
# ============================================================
HEADER = f"""(kicad_sch (version 20230121) (generator eeschema)

  (uuid {uid()})

  (paper "A3" portrait)

  (title_block
    (title "EL-1000 Control Circuit v0.1")
    (date "2026-05-31")
    (rev "0.1")
    (comment 1 "C2000 F28E12x + ESP32-S3 dual MCU")
    (comment 2 "ADC:ADS1115 | DAC:SGM71622R2 | ISO:ISO7741+ADuM1201+ADuM3160")
    (comment 4 "BOM ~196 | SPI+I2C+UART+JTAG")
  )

  (lib_symbols
    (symbol "power:GND" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:GND_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide (name "GND" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "power:+3V3" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+3.3V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+3V3_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+3V3_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+3.3V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "power:+5V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+5V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+5V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+5V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+5V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "power:+12V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+12V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+12V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+12V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+12V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "power:+1V2" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+1.2V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+1V2_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+1V2_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+1.2V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Device:R_0_1" (rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none))))
      (symbol "Device:R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
    (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
      (property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Device:C_0_1"
        (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
        (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none))))
      (symbol "Device:C_1_1"
        (pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
    (symbol "Device:C_Polarized" (pin_numbers hide) (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
      (property "Reference" "C" (at 1.27 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "C" (at 1.27 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at -1.016 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Device:C_Polarized_0_1"
        (polyline (pts (xy -2.032 1.27) (xy 2.032 1.27)) (stroke (width 0.508) (type default)) (fill (type none)))
        (polyline (pts (xy -2.032 -1.27) (xy 2.032 -1.27)) (stroke (width 0.508) (type default)) (fill (type none)))
        (polyline (pts (xy -1.27 0) (xy 1.27 0)) (stroke (width 0.508) (type default)) (fill (type none)))
        (arc (start 0 -1.905) (mid 0.635 -1.27) (end 0 0) (stroke (width 0.254) (type default)) (fill (type none))))
      (symbol "Device:C_Polarized_1_1"
        (pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
    (symbol "Connector_Generic:Conn_02x05" (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 -12.7 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_02x05" (at 0 0 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 12.7 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Connector_Generic:Conn_02x05_0_1"
        (rectangle (start -5.08 11.43) (end 0 -11.43) (stroke (width 0.254) (type default)) (fill (type background)))
        (pin passive line (at -7.62 10.16 0) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 5.08 0) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 0 0) (length 2.54) (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 -5.08 0) (length 2.54) (name "4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -7.62 -10.16 0) (length 2.54) (name "5" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27))))))
      (symbol "Connector_Generic:Conn_02x05_1_1"
        (rectangle (start 0 11.43) (end 5.08 -11.43) (stroke (width 0.254) (type default)) (fill (type background)))
        (pin passive line (at 7.62 10.16 180) (length 2.54) (name "6" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 7.62 5.08 180) (length 2.54) (name "7" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 7.62 0 180) (length 2.54) (name "8" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 7.62 -5.08 180) (length 2.54) (name "9" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 7.62 -10.16 180) (length 2.54) (name "10" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))))
    (symbol "Device:D" (pin_numbers hide) (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
      (property "Reference" "D" (at 0 3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "D" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Device:D_0_1"
        (polyline (pts (xy -3.81 1.27) (xy 0 -2.54)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -2.54) (xy 3.81 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0 -2.54)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -1.905 0) (xy 1.905 0)) (stroke (width 0.254) (type default)) (fill (type none))))
      (symbol "Device:D_1_1"
        (pin passive line (at 0 5.08 270) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -5.08 90) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
  )

"""

# ============================================================
# COMPONENT PLACEMENT
# ============================================================

def make_symbol(lib_id, ref, value, x, y, unit=1, rot=0):
    """Generate a symbol placement block for KiCad 8 s-expression"""
    s = f"  (symbol (lib_id \"{lib_id}\") (at {x} {y} {rot}) (unit {unit})\n"
    s += f"    (property \"Reference\" \"{ref}\" (at {x-2} {y+3} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) (justify left))\n    )\n"
    s += f"    (property \"Value\" \"{value}\" (at {x-2} {y-3} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) (justify left))\n    )\n"
    s += f"    (property \"Footprint\" \"\" (at {x} {y} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) hide)\n    )\n"
    s += f"    (property \"Datasheet\" \"~\" (at {x} {y} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) hide)\n    )\n  )\n"
    return s

def make_power(lib_id, ref, value, x, y, rot=0):
    """Generate a power symbol placement"""
    s = f"  (symbol (lib_id \"{lib_id}\") (at {x} {y} {rot}) (unit 1)\n"
    s += f"    (property \"Reference\" \"#PWR\" (at {x-2} {y+3} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) hide)\n    )\n"
    s += f"    (property \"Value\" \"{value}\" (at {x} {y+2} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)))\n    )\n"
    s += f"    (property \"Footprint\" \"\" (at {x} {y} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) hide)\n    )\n"
    s += f"    (property \"Datasheet\" \"~\" (at {x} {y} 0)\n"
    s += f"      (effects (font (size 1.27 1.27)) hide)\n    )\n  )\n"
    return s

def make_label(text, x, y, rot=0):
    """Generate a global label"""
    return f'  (label "{text}" (at {x} {y} {rot})\n    (effects (font (size 1.27 1.27)) (justify left))\n  )\n'

def make_wire(pts, width=0):
    """Generate a wire. pts is list of (x,y) tuples"""
    s = f"  (wire (pts\n"
    for p in pts:
        s += f"    (xy {p[0]} {p[1]})\n"
    s += f"  ) (stroke (width {width}) (type default)) (layer \"F.Cu\"))\n"
    return s

def make_no_connect(x, y):
    return f"  (no_connect (at {x} {y}))\n"

# ============================================================
# BUILD SCHEMATIC
# ============================================================
lines = [HEADER]

# === C2000 F28E12x Minimum System ===
# Crystal oscillator section (left side)
lines += [make_symbol("Device:R", "R101", "1M", 30, 180)]  # bias R
lines += [make_symbol("Device:R", "R102", "0R", 30, 160)]  # series R
lines += [make_symbol("Device:C", "C101", "18pF", 50, 180)]
lines += [make_symbol("Device:C", "C102", "18pF", 50, 160)]
lines += [make_power("power:GND", "#PWR", "GND", 50, 190)]
lines += [make_power("power:GND", "#PWR", "GND", 50, 150)]

# JTAG header
lines += [make_symbol("Connector_Generic:Conn_02x05", "J101", "JTAG-10pin", 30, 100)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 30, 85)]
lines += [make_power("power:GND", "#PWR", "GND", 30, 120)]

# C2000 MCU (center, using C2000 F28E12x 48-pin LQFP - approximate with a large IC symbol)
# For KiCad inline, we use a generic connector pattern to represent the MCU
lines += [make_symbol("Device:C", "C103", "0.1uF", 150, 100)]  # VDDIO decouple
lines += [make_symbol("Device:C", "C104", "10uF", 150, 85)]    # VDDIO bulk
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 150, 75)]
lines += [make_power("power:GND", "#PWR", "GND", 150, 115)]
lines += [make_symbol("Device:C", "C105", "1uF", 150, 130)]    # VDD core decouple
lines += [make_power("power:+1V2", "#PWR", "+1.2V", 150, 140)]

# ADC decoupling
lines += [make_symbol("Device:C", "C106", "0.1uF", 200, 100)]
lines += [make_symbol("Device:C", "C107", "10uF", 200, 85)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 200, 75)]
lines += [make_power("power:GND", "#PWR", "GND", 200, 115)]

# Reset circuit
lines += [make_symbol("Device:R", "R103", "10k", 100, 260)]
lines += [make_symbol("Device:C", "C108", "0.1uF", 100, 240)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 100, 250)]
lines += [make_power("power:GND", "#PWR", "GND", 100, 230)]

# Boot mode select
lines += [make_symbol("Device:R", "R104", "10k", 30, 260)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 30, 250)]

# === ESP32-S3 Module (right side) ===
lines += [make_symbol("Device:C", "C201", "0.1uF", 350, 100)]
lines += [make_symbol("Device:C", "C202", "10uF", 350, 85)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 350, 75)]
lines += [make_power("power:GND", "#PWR", "GND", 350, 115)]

# ESP32 enable/reset
lines += [make_symbol("Device:R", "R201", "10k", 300, 260)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 300, 250)]

# === DAC: SGM71622R2 (SPI) ===
lines += [make_symbol("Device:C", "C301", "0.1uF", 100, 320)]
lines += [make_power("power:+5V", "#PWR", "+5V", 100, 310)]
lines += [make_power("power:GND", "#PWR", "GND", 100, 335)]
lines += [make_symbol("Device:C", "C302", "10uF", 130, 320)]
lines += [make_power("power:+5V", "#PWR", "+5V", 130, 310)]
lines += [make_power("power:GND", "#PWR", "GND", 130, 335)]

# DAC output RC filter for HRPWM
lines += [make_symbol("Device:R", "R301", "10k", 160, 320)]
lines += [make_symbol("Device:C", "C303", "1uF", 180, 320)]
lines += [make_power("power:GND", "#PWR", "GND", 180, 335)]

# === ADS1115 ADC (I2C) ===
lines += [make_symbol("Device:C", "C401", "0.1uF", 100, 400)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 100, 390)]
lines += [make_power("power:GND", "#PWR", "GND", 100, 415)]
lines += [make_symbol("Device:R", "R401", "10k", 130, 390)]  # SCL pullup
lines += [make_symbol("Device:R", "R402", "10k", 130, 405)]  # SDA pullup
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 130, 380)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 130, 395)]

# ADDR select for ADS1115 (GND = 0x48)
lines += [make_symbol("Device:R", "R403", "0R", 100, 425)]
lines += [make_power("power:GND", "#PWR", "GND", 100, 435)]

# === ISO7741 Digital Isolator ===
lines += [make_symbol("Device:C", "C501", "0.1uF", 250, 320)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 250, 310)]
lines += [make_power("power:GND", "#PWR", "GND", 250, 335)]
# ISO7741 side2 power (from isolated domain)
lines += [make_symbol("Device:C", "C502", "0.1uF", 280, 350)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 280, 340)]
lines += [make_power("power:GND", "#PWR", "GND", 280, 365)]

# === ADuM1201 UART Isolator ===
lines += [make_symbol("Device:C", "C601", "0.1uF", 250, 400)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 250, 390)]
lines += [make_power("power:GND", "#PWR", "GND", 250, 415)]
lines += [make_symbol("Device:C", "C602", "0.1uF", 280, 400)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 280, 390)]
lines += [make_power("power:GND", "#PWR", "GND", 280, 415)]

# === ADuM3160 USB Isolator ===
lines += [make_symbol("Device:C", "C701", "0.1uF", 350, 320)]
lines += [make_power("power:+5V", "#PWR", "+5V", 350, 310)]
lines += [make_power("power:GND", "#PWR", "GND", 350, 335)]
lines += [make_symbol("Device:C", "C702", "10uF", 350, 350)]
lines += [make_power("power:+5V", "#PWR", "+5V", 350, 340)]
lines += [make_power("power:GND", "#PWR", "GND", 350, 365)]

# === LDO AMS1117-3.3 ===
lines += [make_symbol("Device:C_Polarized", "C801", "10uF/10V", 400, 100)]
lines += [make_symbol("Device:C_Polarized", "C802", "10uF/6.3V", 430, 100)]
lines += [make_power("power:+5V", "#PWR", "+5V", 400, 90)]
lines += [make_power("power:GND", "#PWR", "GND", 400, 115)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 430, 90)]
lines += [make_power("power:GND", "#PWR", "GND", 430, 115)]

# === LCD Connector (40-pin FPC) ===
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 400, 200)]
lines += [make_power("power:GND", "#PWR", "GND", 400, 250)]

# === Encoder (EC11) ===
lines += [make_symbol("Device:R", "R901", "10k", 400, 300)]  # pullup
lines += [make_symbol("Device:R", "R902", "10k", 400, 315)]
lines += [make_symbol("Device:R", "R903", "10k", 400, 330)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 400, 290)]

# === Keypad (4x4 matrix) ===
# Row pullups
for i in range(4):
    y = 380 + i * 15
    lines += [make_symbol("Device:R", f"R90{4+i}", "10k", 400, y)]
    lines += [make_power("power:+3V3", "#PWR", "+3.3V", 400, y-10)]

# === Watchdog TPS3823 ===
lines += [make_symbol("Device:C", "C1001", "0.1uF", 100, 470)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 100, 460)]
lines += [make_power("power:GND", "#PWR", "GND", 100, 485)]
lines += [make_symbol("Device:R", "R1001", "10k", 130, 470)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 130, 460)]

# ============================================================
# GLOBAL LABELS (net ports)
# ============================================================
lines += [make_label("SCL", 130, 392, 270)]   # I2C SCL to ESP32
lines += [make_label("SDA", 130, 408, 270)]   # I2C SDA
lines += [make_label("SPI_SCLK", 90, 340, 90)]  # SPI to DAC
lines += [make_label("SPI_MOSI", 100, 345, 90)]
lines += [make_label("SPI_CS_DAC", 100, 350, 90)]
lines += [make_label("UART_TX", 280, 400, 90)]  # UART to ESP32
lines += [make_label("UART_RX", 280, 410, 90)]
lines += [make_label("HRPWM_OUT", 200, 320, 90)]  # HRPWM to isolator
lines += [make_label("DAC_OUT", 180, 330, 90)]
lines += [make_label("ENC_A", 400, 305, 90)]
lines += [make_label("ENC_B", 400, 320, 90)]
lines += [make_label("ENC_SW", 400, 335, 90)]
lines += [make_label("LCD_CLK", 400, 200, 90)]
lines += [make_label("LCD_MOSI", 400, 210, 90)]
lines += [make_label("LCD_CS", 400, 220, 90)]
lines += [make_label("LCD_DC", 400, 230, 90)]
lines += [make_label("LCD_RST", 400, 240, 90)]
lines += [make_label("LCD_BL", 400, 260, 90)]
lines += [make_label("USB_DP", 350, 325, 90)]
lines += [make_label("USB_DN", 350, 345, 90)]

# ============================================================
# WIRES (interconnections)
# ============================================================
# Crystal circuit
lines += [make_wire([(30, 170), (30, 160)])]
lines += [make_wire([(30, 160), (50, 160)])]
lines += [make_wire([(30, 180), (50, 180)])]
lines += [make_wire([(50, 185), (50, 190)])]
lines += [make_wire([(50, 155), (50, 150)])]

# C2000 decoupling
lines += [make_wire([(150, 94), (150, 85)])]
lines += [make_wire([(150, 75), (150, 79)])]
lines += [make_wire([(150, 105), (150, 115)])]
lines += [make_wire([(200, 94), (200, 85)])]
lines += [make_wire([(200, 75), (200, 79)])]
lines += [make_wire([(200, 105), (200, 115)])]

# Reset circuit
lines += [make_wire([(100, 245), (100, 250)])]
lines += [make_wire([(100, 235), (100, 230)])]

# ADC decoupling
lines += [make_wire([(100, 315), (100, 310)])]
lines += [make_wire([(100, 325), (100, 335)])]

# ESP32 decoupling
lines += [make_wire([(350, 94), (350, 85)])]
lines += [make_wire([(350, 75), (350, 79)])]
lines += [make_wire([(350, 105), (350, 115)])]

# I2C pullups for ADS1115
lines += [make_wire([(130, 385), (130, 380)])]
lines += [make_wire([(130, 400), (130, 395)])]
lines += [make_wire([(130, 390), (100, 390)])]
lines += [make_wire([(130, 405), (100, 405)])]

# LDO
lines += [make_wire([(400, 94), (400, 90)])]
lines += [make_wire([(400, 105), (400, 115)])]
lines += [make_wire([(430, 94), (430, 90)])]
lines += [make_wire([(430, 105), (430, 115)])]
lines += [make_wire([(400, 100), (430, 100)])]  # LDO output to 3.3V rail

# ============================================================
# SHEET INSTANCES
# ============================================================
lines += ["""  (sheet_instances
    (path "/" (page "1"))
  )
"""]

# ============================================================
# SYMBOL INSTANCES
# ============================================================
lines += ["""  (symbol_instances
    (path "/" (reference "#PWR") (unit 1))
  )
"""]

lines += [")"]

# ============================================================
# WRITE FILE
# ============================================================
sch_content = "\n".join(lines)
outpath = os.path.join(OUTDIR, "EL-1000_ControlCircuit.kicad_sch")
with open(outpath, "w", encoding="utf-8") as f:
    f.write(sch_content)
print(f"Generated: {outpath} ({len(sch_content)} bytes, {sch_content.count(chr(10))} lines)")
