#!/usr/bin/env python3
"""
Generate EL-1000 Power Tree schematic (.kicad_sch)
Based on SYS-SCH-003 v0.1 design document

Contains:
  - AC input + EMI filter + rectifier
  - Flyback converter (UCC28C45)
  - Buck1: +15V/1A
  - Buck2: +12V/2A
  - Buck3: +5V/3A
  - LDO 3.3V
  - -15V charge pump
"""

import uuid, os

OUTDIR = os.path.dirname(os.path.abspath(__file__))

def uid():
    return str(uuid.uuid4()).upper()

HEADER = f"""(kicad_sch (version 20230121) (generator eeschema)

  (uuid {uid()})

  (paper "A3" landscape)

  (title_block
    (title "EL-1000 Power Tree v0.1")
    (date "2026-05-31")
    (rev "0.1")
    (comment 1 "AC220V->EMI->Rect->Flyback(48V)->Buck1/2/3->LDO")
    (comment 2 "UCC28C45 | 65kHz CCM flyback | 3x Buck(HRPWM) | Charge pump(-15V)")
    (comment 4 "BOM ~148 | flyback sub-board + mainboard Buck")
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
    (symbol "power:+310V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+310V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+310V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+310V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+310V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "power:+48V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+48V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+48V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+48V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+48V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
    (symbol "power:+15V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "+15V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:+15V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:+15V_1_1"
        (pin power_in line (at 0 0 90) (length 0) hide (name "+15V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
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
    (symbol "power:-15V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
      (property "Value" "-15V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "power:-15V_0_1"
        (polyline (pts (xy -0.762 -1.27) (xy 0 -2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 -2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -2.54) (xy 0.762 -1.27)) (stroke (width 0) (type default)) (fill (type none))))
      (symbol "power:-15V_1_1"
        (pin power_in line (at 0 0 270) (length 0) hide (name "-15V" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))))
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
    (symbol "Device:D_Zener" (pin_numbers hide) (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
      (property "Reference" "D" (at 0 3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "D" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Device:D_Zener_0_1"
        (polyline (pts (xy -3.81 1.27) (xy 0 -2.54)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -2.54) (xy 3.81 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0 -2.54)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -1.905 0) (xy 1.905 0)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -0.635 -1.27) (xy 0.635 -1.27)) (stroke (width 0.254) (type default)) (fill (type none))))
      (symbol "Device:D_Zener_1_1"
        (pin passive line (at 0 5.08 270) (length 2.54) (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -5.08 90) (length 2.54) (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
    (symbol "Device:L" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "L" (at 0 -0.635 0) (effects (font (size 1.27 1.27))))
      (property "Value" "L" (at 0 -3.175 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Device:L_0_1"
        (polyline (pts (xy -2.54 0.635) (xy -2.54 2.54) (xy 2.54 2.54) (xy 2.54 0.635)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -1.27 -0.635) (xy -1.27 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -0.635) (xy 0 2.54)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 1.27 -0.635) (xy 1.27 2.54)) (stroke (width 0.254) (type default)) (fill (type none))))
      (symbol "Device:L_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))
    (symbol "Transistor_FET:IRF9540" (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
      (property "Reference" "Q" (at 2.54 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "IRF9540" (at 2.54 -2.54 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_TO_SOT_THT:TO-220-3_Vertical" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Transistor_FET:IRF9540_0_1"
        (rectangle (start 0.635 -5.08) (end 5.08 5.08) (stroke (width 0.254) (type default)) (fill (type background)))
        (polyline (pts (xy 0.635 -3.81) (xy -1.27 -1.905) (xy 0.635 0)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -1.27 0) (xy 0.635 0)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -0.635 -3.175) (xy 0.635 -3.175)) (stroke (width 0.254) (type default)) (fill (type none))))
      (symbol "Transistor_FET:IRF9540_1_1"
        (pin passive line (at -2.54 0 0) (length 1.905) (name "S" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -2.54 3.81 0) (length 1.905) (name "G" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 7.62 0 180) (length 2.54) (name "D" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))))
  )

"""

def make_symbol(lib_id, ref, value, x, y, unit=1, rot=0):
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
    return f'  (label "{text}" (at {x} {y} {rot})\n    (effects (font (size 1.27 1.27)) (justify left))\n  )\n'

def make_wire(pts, width=0):
    s = f"  (wire (pts\n"
    for p in pts:
        s += f"    (xy {p[0]} {p[1]})\n"
    s += f"  ) (stroke (width {width}) (type default)) (layer \"F.Cu\"))\n"
    return s

# ============================================================
# BUILD
# ============================================================
lines = [HEADER]

# === AC Input Section (left) ===
# IEC C14 + Fuse
lines += [make_symbol("Device:R", "R1", "NTC 5R", 20, 50)]      # NTC
lines += [make_symbol("Device:R", "R2", "100k 2W", 20, 80)]     # bleeder
lines += [make_power("power:+310V", "#PWR", "+310V", 20, 70)]    # Note: this is bus label
lines += [make_power("power:GND", "#PWR", "GND", 20, 90)]

# EMI filter components
lines += [make_symbol("Device:C", "CX1", "0.22uF X2", 50, 50)]  # X cap
lines += [make_symbol("Device:C", "CY1", "2.2nF Y2", 50, 30)]
lines += [make_symbol("Device:C", "CY2", "2.2nF Y2", 50, 70)]
lines += [make_power("power:GND", "#PWR", "GND", 50, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 50, 80)]

# Common mode choke
lines += [make_symbol("Device:L", "L1", "20mH 2A", 80, 50)]

# Rectifier output + bus cap
lines += [make_symbol("Device:C_Polarized", "CB1", "120uF 400V", 110, 50)]
lines += [make_power("power:+310V", "#PWR", "+310V", 110, 40)]
lines += [make_power("power:GND", "#PWR", "GND", 110, 65)]

# === Flyback Converter (UCC28C45) — center-left ===
# Flyback MOSFET
lines += [make_symbol("Device:R", "R3", "4.7k+TypeII", 170, 30)]  # COMP
lines += [make_symbol("Device:C", "C1", "0.1uF", 170, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 170, 10)]
lines += [make_symbol("Device:C", "C2", "4.7nF", 170, 45)]

# CS resistor
lines += [make_symbol("Device:R", "R4", "0.5R 1W", 200, 70)]
lines += [make_symbol("Device:R", "R5", "220R", 200, 55)]
lines += [make_symbol("Device:C", "C3", "1nF", 200, 40)]
lines += [make_power("power:GND", "#PWR", "GND", 200, 85)]
lines += [make_power("power:GND", "#PWR", "GND", 200, 35)]

# RT/CT frequency set
lines += [make_symbol("Device:R", "R6", "12k", 230, 70)]
lines += [make_symbol("Device:C", "C4", "1nF", 230, 55)]
lines += [make_power("power:GND", "#PWR", "GND", 230, 45)]

# Gate drive
lines += [make_symbol("Device:R", "R7", "10R", 170, 100)]
lines += [make_symbol("Device:D", "D1", "1N4148", 190, 100)]

# VCC startup
lines += [make_symbol("Device:R", "R8", "47k 2W", 140, 100)]
lines += [make_power("power:+310V", "#PWR", "+310V", 140, 90)]

# Flyback transformer representation (output section)
lines += [make_symbol("Device:C_Polarized", "C5", "1000uF 63V", 230, 110)]
lines += [make_symbol("Device:C_Polarized", "C6", "1000uF 63V", 260, 110)]
lines += [make_power("power:GND", "#PWR", "GND", 230, 125)]
lines += [make_power("power:GND", "#PWR", "GND", 260, 125)]

# Feedback (TL431 + PC817)
lines += [make_symbol("Device:R", "R9", "2.5k", 290, 70)]
lines += [make_symbol("Device:R", "R10", "10k", 290, 90)]
lines += [make_symbol("Device:C", "C7", "0.1uF", 290, 105)]
lines += [make_power("power:+48V", "#PWR", "+48V", 290, 60)]

# === Buck1: +15V/1A (P-MOS, no bootstrap) ===
lines += [make_symbol("Transistor_FET:IRF9540", "Q1", "IRF9540", 350, 30)]
lines += [make_symbol("Device:D", "D2", "SS34", 350, 60)]
lines += [make_symbol("Device:L", "L2", "33uH", 380, 30)]
lines += [make_symbol("Device:C_Polarized", "C8", "22uF+100uF", 410, 30)]
lines += [make_power("power:+48V", "#PWR", "+48V", 350, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 350, 75)]
lines += [make_power("power:+15V", "#PWR", "+15V", 410, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 410, 45)]

# === Buck2: +12V/2A (N-MOS + bootstrap) ===
lines += [make_symbol("Device:R", "R11", "10R", 470, 30)]  # gate R
lines += [make_symbol("Device:D", "D3", "1N4148", 470, 45)]  # bootstrap diode
lines += [make_symbol("Device:C", "C9", "0.1uF", 490, 45)]  # bootstrap cap
lines += [make_symbol("Device:C", "C10", "1uF", 490, 60)]
lines += [make_symbol("Device:D", "D4", "SS34", 500, 30)]  # freewheel
lines += [make_symbol("Device:L", "L3", "47uH", 530, 30)]
lines += [make_symbol("Device:C_Polarized", "C11", "220uF 25V", 560, 30)]
lines += [make_power("power:+48V", "#PWR", "+48V", 470, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 500, 45)]
lines += [make_power("power:+12V", "#PWR", "+12V", 560, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 560, 45)]

# === Buck3: +5V/3A (N-MOS + bootstrap) ===
lines += [make_symbol("Device:R", "R12", "10R", 350, 140)]  # gate R
lines += [make_symbol("Device:D", "D5", "1N4148", 350, 155)]  # bootstrap
lines += [make_symbol("Device:C", "C12", "0.1uF", 370, 155)]
lines += [make_symbol("Device:D", "D6", "SS14", 380, 140)]  # freewheel
lines += [make_symbol("Device:L", "L4", "10uH", 410, 140)]
lines += [make_symbol("Device:C", "C13", "10uF", 440, 140)]
lines += [make_symbol("Device:C", "C14", "10uF", 460, 140)]
lines += [make_symbol("Device:C", "C15", "10uF", 480, 140)]
lines += [make_power("power:+48V", "#PWR", "+48V", 350, 130)]
lines += [make_power("power:GND", "#PWR", "GND", 380, 155)]
lines += [make_power("power:+5V", "#PWR", "+5V", 440, 130)]
lines += [make_power("power:+5V", "#PWR", "+5V", 460, 130)]
lines += [make_power("power:+5V", "#PWR", "+5V", 480, 130)]
lines += [make_power("power:GND", "#PWR", "GND", 440, 155)]
lines += [make_power("power:GND", "#PWR", "GND", 460, 155)]
lines += [make_power("power:GND", "#PWR", "GND", 480, 155)]

# === LDO: AMS1117-3.3 ===
lines += [make_symbol("Device:C_Polarized", "C16", "10uF 10V", 530, 140)]
lines += [make_symbol("Device:C_Polarized", "C17", "10uF 6.3V", 560, 140)]
lines += [make_power("power:+5V", "#PWR", "+5V", 530, 130)]
lines += [make_power("power:GND", "#PWR", "GND", 530, 155)]
lines += [make_power("power:+3V3", "#PWR", "+3.3V", 560, 130)]
lines += [make_power("power:GND", "#PWR", "GND", 560, 155)]

# === -15V Charge Pump ===
lines += [make_symbol("Device:D", "D7", "1N4148", 630, 30)]
lines += [make_symbol("Device:D", "D8", "1N4148", 630, 55)]
lines += [make_symbol("Device:C", "C18", "10uF", 660, 30)]
lines += [make_symbol("Device:C", "C19", "10uF", 660, 55)]
lines += [make_power("power:+15V", "#PWR", "+15V", 630, 20)]
lines += [make_power("power:GND", "#PWR", "GND", 660, 45)]
lines += [make_power("power:-15V", "#PWR", "-15V", 660, 65)]

# ============================================================
# GLOBAL LABELS
# ============================================================
lines += [make_label("HRPWM_BUCK1", 350, 25, 270)]
lines += [make_label("HRPWM_BUCK2", 470, 25, 270)]
lines += [make_label("HRPWM_BUCK3", 350, 135, 270)]
lines += [make_label("HRPWM_CHPUMP", 630, 25, 270)]
lines += [make_label("FLYBACK_GATE", 170, 105, 90)]
lines += [make_label("AC_L", 20, 40, 0)]
lines += [make_label("AC_N", 20, 60, 0)]
lines += [make_label("VREF_5V", 290, 75, 90)]

# ============================================================
# WIRES
# ============================================================
# AC input chain
lines += [make_wire([(20, 50), (50, 50)])]
lines += [make_wire([(50, 50), (80, 50)])]
lines += [make_wire([(80, 50), (110, 50)])]
lines += [make_wire([(110, 45), (110, 40)])]
lines += [make_wire([(110, 60), (110, 65)])]

# Flyback
lines += [make_wire([(170, 35), (170, 20)])]
lines += [make_wire([(170, 10), (170, 14)])]
lines += [make_wire([(200, 65), (200, 55)])]
lines += [make_wire([(200, 50), (200, 40)])]
lines += [make_wire([(200, 35), (200, 34)])]
lines += [make_wire([(200, 80), (200, 85)])]
lines += [make_wire([(230, 65), (230, 55)])]
lines += [make_wire([(230, 50), (230, 45)])]
lines += [make_wire([(170, 100), (190, 100)])]
lines += [make_wire([(140, 95), (140, 90)])]

# Flyback output
lines += [make_wire([(230, 105), (230, 125)])]
lines += [make_wire([(260, 105), (260, 125)])]

# Feedback
lines += [make_wire([(290, 75), (290, 85)])]
lines += [make_wire([(290, 65), (290, 60)])]

# Buck1
lines += [make_wire([(350, 55), (350, 60)])]
lines += [make_wire([(350, 65), (350, 75)])]
lines += [make_wire([(350, 40), (380, 30)])]
lines += [make_wire([(380, 30), (410, 30)])]
lines += [make_wire([(410, 25), (410, 20)])]
lines += [make_wire([(410, 40), (410, 45)])]

# Buck2
lines += [make_wire([(470, 35), (500, 30)])]
lines += [make_wire([(500, 30), (530, 30)])]
lines += [make_wire([(530, 30), (560, 30)])]
lines += [make_wire([(560, 25), (560, 20)])]
lines += [make_wire([(560, 40), (560, 45)])]
lines += [make_wire([(490, 50), (490, 60)])]

# Buck3
lines += [make_wire([(350, 145), (380, 140)])]
lines += [make_wire([(380, 140), (410, 140)])]
lines += [make_wire([(410, 140), (440, 140), (460, 140), (480, 140)])]
lines += [make_wire([(440, 135), (440, 130)])]
lines += [make_wire([(440, 150), (440, 155)])]

# LDO
lines += [make_wire([(530, 135), (530, 130)])]
lines += [make_wire([(530, 150), (530, 155)])]
lines += [make_wire([(530, 140), (560, 140)])]
lines += [make_wire([(560, 135), (560, 130)])]
lines += [make_wire([(560, 150), (560, 155)])]

# Charge pump
lines += [make_wire([(630, 35), (630, 20)])]
lines += [make_wire([(630, 40), (630, 50)])]
lines += [make_wire([(630, 60), (660, 30)])]
lines += [make_wire([(660, 35), (660, 45)])]
lines += [make_wire([(660, 60), (660, 65)])]

# ============================================================
# SHEET+SYMBOL INSTANCES
# ============================================================
lines += ["""  (sheet_instances
    (path "/" (page "1"))
  )
"""]

lines += ["""  (symbol_instances
    (path "/" (reference "#PWR") (unit 1))
  )
"""]

lines += [")"]

sch_content = "\n".join(lines)
outpath = os.path.join(OUTDIR, "EL-1000_PowerTree.kicad_sch")
with open(outpath, "w", encoding="utf-8") as f:
    f.write(sch_content)
print(f"Generated: {outpath} ({len(sch_content)} bytes, {sch_content.count(chr(10))} lines)")
