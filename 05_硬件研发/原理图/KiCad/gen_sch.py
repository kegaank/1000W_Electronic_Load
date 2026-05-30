#!/usr/bin/env python3
"""Generate EL-1000 Power Stage KiCad 7 schematic (.kicad_sch)"""

import uuid

def uid():
    return str(uuid.uuid4()).upper()

# ============================================================
# SYMBOL DEFINITIONS (extracted from KiCad libraries)
# ============================================================

SYM_R = r'''  (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "R" (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "R" (at 0 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at -1.778 0 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "R res resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Resistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "R_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Device:R_0_1"
      (rectangle (start -1.016 -2.54) (end 1.016 2.54)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
    )
    (symbol "Device:R_1_1"
      (pin passive line (at 0 3.81 270) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 1.27)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_C = r'''  (symbol "Device:C" (pin_numbers hide) (pin_names (offset 0.254)) (in_bom yes) (on_board yes)
    (property "Reference" "C" (at 0.635 2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "C" (at 0.635 -2.54 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "" (at 0.9652 -3.81 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "cap capacitor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Unpolarized capacitor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "C_*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Device:C_0_1"
      (polyline
        (pts
          (xy -2.032 -0.762)
          (xy 2.032 -0.762)
        )
        (stroke (width 0.508) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy -2.032 0.762)
          (xy 2.032 0.762)
        )
        (stroke (width 0.508) (type default))
        (fill (type none))
      )
    )
    (symbol "Device:C_1_1"
      (pin passive line (at 0 3.81 270) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 0 -3.81 90) (length 2.794)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_GND = r'''  (symbol "power:GND" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (at 0 -6.35 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "global power" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"GND\" , ground" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "power:GND_0_1"
      (polyline
        (pts
          (xy 0 0)
          (xy 0 -1.27)
          (xy 1.27 -1.27)
          (xy 0 -2.54)
          (xy -1.27 -1.27)
          (xy 0 -1.27)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
    )
    (symbol "power:GND_1_1"
      (pin power_in line (at 0 0 270) (length 0) hide
        (name "GND" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_5V = r'''  (symbol "power:+5V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "+5V" (at 0 3.556 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "global power" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"+5V\"" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "power:+5V_0_1"
      (polyline
        (pts
          (xy -0.762 1.27)
          (xy 0 2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 0)
          (xy 0 2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 2.54)
          (xy 0.762 1.27)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
    )
    (symbol "power:+5V_1_1"
      (pin power_in line (at 0 0 90) (length 0) hide
        (name "+5V" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_15V = r'''  (symbol "power:+15V" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
    (property "Reference" "#PWR" (at 0 -3.81 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "+15V" (at 0 3.556 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "global power" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Power symbol creates a global label with name \"+15V\"" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "power:+15V_0_1"
      (polyline
        (pts
          (xy -0.762 1.27)
          (xy 0 2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 0)
          (xy 0 2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0 2.54)
          (xy 0.762 1.27)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
    )
    (symbol "power:+15V_1_1"
      (pin power_in line (at 0 0 90) (length 0) hide
        (name "+15V" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_LM358 = r'''  (symbol "Amplifier_Operational:LM358" (pin_names (offset 0.127)) (in_bom yes) (on_board yes)
    (property "Reference" "U" (at 0 5.08 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "LM358" (at 0 -5.08 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "http://www.ti.com/lit/ds/symlink/lm358.pdf" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "dual opamp" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "Dual Operational Amplifiers, DIP-8/SOIC-8/TSSOP-8/VSSOP-8" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "SOIC*3.9x4.9mm*P1.27mm* DIP*W7.62mm* TO*99* OnSemi*Micro8* TSSOP*3x3mm*P0.65mm* TSSOP*4.4x3mm*P0.65mm* MSOP*3x3mm*P0.65mm* SSOP*3.9x4.9mm*P0.635mm* LFCSP*2x2mm*P0.5mm* *SIP* SOIC*5.3x6.2mm*P1.27mm*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Amplifier_Operational:LM358_1_1"
      (polyline
        (pts
          (xy -5.08 5.08)
          (xy 5.08 0)
          (xy -5.08 -5.08)
          (xy -5.08 5.08)
        )
        (stroke (width 0.254) (type default))
        (fill (type background))
      )
      (pin output line (at 7.62 0 180) (length 2.54)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -7.62 -2.54 0) (length 2.54)
        (name "-" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -7.62 2.54 0) (length 2.54)
        (name "+" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
    (symbol "Amplifier_Operational:LM358_2_1"
      (polyline
        (pts
          (xy -5.08 5.08)
          (xy 5.08 0)
          (xy -5.08 -5.08)
          (xy -5.08 5.08)
        )
        (stroke (width 0.254) (type default))
        (fill (type background))
      )
      (pin input line (at -7.62 2.54 0) (length 2.54)
        (name "+" (effects (font (size 1.27 1.27))))
        (number "5" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -7.62 -2.54 0) (length 2.54)
        (name "-" (effects (font (size 1.27 1.27))))
        (number "6" (effects (font (size 1.27 1.27))))
      )
      (pin output line (at 7.62 0 180) (length 2.54)
        (name "~" (effects (font (size 1.27 1.27))))
        (number "7" (effects (font (size 1.27 1.27))))
      )
    )
    (symbol "Amplifier_Operational:LM358_3_1"
      (pin power_in line (at -2.54 -7.62 90) (length 3.81)
        (name "V-" (effects (font (size 1.27 1.27))))
        (number "4" (effects (font (size 1.27 1.27))))
      )
      (pin power_in line (at -2.54 7.62 270) (length 3.81)
        (name "V+" (effects (font (size 1.27 1.27))))
        (number "8" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_NPN = r'''  (symbol "Transistor_BJT:D882" (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
    (property "Reference" "Q" (at 5.08 1.905 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "D882" (at 5.08 0 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Package_TO_SOT_THT:TO-126-3_Vertical" (at 5.08 -1.905 0)
      (effects (font (size 1.27 1.27) italic) (justify left) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (justify left) hide)
    )
    (property "ki_keywords" "NPN Transistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "3A Ic, 60V Vce, NPN Power Transistor, TO-126" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "TO?126*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Transistor_BJT:D882_0_1"
      (polyline
        (pts
          (xy 0.635 0.635)
          (xy 2.54 2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.635 -0.635)
          (xy 2.54 -2.54)
          (xy 2.54 -2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.635 1.905)
          (xy 0.635 -1.905)
          (xy 0.635 -1.905)
        )
        (stroke (width 0.508) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 1.27 -1.778)
          (xy 1.778 -1.27)
          (xy 2.286 -2.286)
          (xy 1.27 -1.778)
          (xy 1.27 -1.778)
        )
        (stroke (width 0) (type default))
        (fill (type outline))
      )
      (circle (center 1.27 0) (radius 2.8194)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
    )
    (symbol "Transistor_BJT:D882_1_1"
      (pin passive line (at 2.54 -5.08 90) (length 2.54)
        (name "E" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at -5.08 0 0) (length 5.715)
        (name "B" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 2.54 5.08 270) (length 2.54)
        (name "C" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_PNP = r'''  (symbol "Transistor_BJT:B772" (pin_names (offset 0) hide) (in_bom yes) (on_board yes)
    (property "Reference" "Q" (at 5.08 1.905 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "B772" (at 5.08 0 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Package_TO_SOT_THT:TO-126-3_Vertical" (at 5.08 -1.905 0)
      (effects (font (size 1.27 1.27) italic) (justify left) hide)
    )
    (property "Datasheet" "~" (at 0 0 0)
      (effects (font (size 1.27 1.27)) (justify left) hide)
    )
    (property "ki_keywords" "PNP Transistor" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "-3A Ic, -60V Vce, PNP Power Transistor, TO-126" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "TO?126*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Transistor_BJT:B772_0_1"
      (polyline
        (pts
          (xy 0.635 0.635)
          (xy 2.54 2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.635 -0.635)
          (xy 2.54 -2.54)
          (xy 2.54 -2.54)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.635 1.905)
          (xy 0.635 -1.905)
          (xy 0.635 -1.905)
        )
        (stroke (width 0.508) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 2.286 -1.778)
          (xy 1.778 -2.286)
          (xy 1.27 -1.27)
          (xy 2.286 -1.778)
          (xy 2.286 -1.778)
        )
        (stroke (width 0) (type default))
        (fill (type outline))
      )
      (circle (center 1.27 0) (radius 2.8194)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
    )
    (symbol "Transistor_BJT:B772_1_1"
      (pin passive line (at 2.54 -5.08 90) (length 2.54)
        (name "E" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin input line (at -5.08 0 0) (length 5.715)
        (name "B" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 2.54 5.08 270) (length 2.54)
        (name "C" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_NMOS = r'''  (symbol "Transistor_FET:M90N20" (pin_names hide) (in_bom yes) (on_board yes)
    (property "Reference" "Q" (at 5.08 1.905 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "M90N20" (at 5.08 0 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Package_TO_SOT_THT:TO-247-3_Vertical" (at 5.08 -1.905 0)
      (effects (font (size 1.27 1.27) italic) (justify left) hide)
    )
    (property "Datasheet" "~" (at 5.08 -3.81 0)
      (effects (font (size 1.27 1.27)) (justify left) hide)
    )
    (property "ki_keywords" "N-Channel Power MOSFET" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "90A Id, 200V Vds, N-Channel Power MOSFET, TO-247" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "TO?247*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Transistor_FET:M90N20_0_1"
      (polyline
        (pts
          (xy 0.254 0)
          (xy -2.54 0)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.254 1.905)
          (xy 0.254 -1.905)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 -1.27)
          (xy 0.762 -2.286)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 0.508)
          (xy 0.762 -0.508)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 2.286)
          (xy 0.762 1.27)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 2.54 2.54)
          (xy 2.54 1.778)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 2.54 -2.54)
          (xy 2.54 0)
          (xy 0.762 0)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 -1.778)
          (xy 3.302 -1.778)
          (xy 3.302 1.778)
          (xy 0.762 1.778)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 1.016 0)
          (xy 2.032 0.381)
          (xy 2.032 -0.381)
          (xy 1.016 0)
        )
        (stroke (width 0) (type default))
        (fill (type outline))
      )
      (polyline
        (pts
          (xy 2.794 0.508)
          (xy 2.921 0.381)
          (xy 3.683 0.381)
          (xy 3.81 0.254)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 3.302 0.381)
          (xy 2.921 -0.254)
          (xy 3.683 -0.254)
          (xy 3.302 0.381)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (circle (center 1.651 0) (radius 2.794)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (circle (center 2.54 -1.778) (radius 0.254)
        (stroke (width 0) (type default))
        (fill (type outline))
      )
      (circle (center 2.54 1.778) (radius 0.254)
        (stroke (width 0) (type default))
        (fill (type outline))
      )
    )
    (symbol "Transistor_FET:M90N20_1_1"
      (pin input line (at -5.08 0 0) (length 2.54)
        (name "G" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 2.54 5.08 270) (length 2.54)
        (name "D" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 2.54 -5.08 90) (length 2.54)
        (name "S" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

SYM_NMOS_PROT = r'''  (symbol "Transistor_FET:2N7002" (pin_names hide) (in_bom yes) (on_board yes)
    (property "Reference" "Q" (at 5.08 1.905 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "2N7002" (at 5.08 0 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 5.08 -1.905 0)
      (effects (font (size 1.27 1.27) italic) (justify left) hide)
    )
    (property "Datasheet" "~" (at 5.08 -3.81 0)
      (effects (font (size 1.27 1.27)) (justify left) hide)
    )
    (property "ki_keywords" "N-Channel MOSFET" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "60V Vds, 0.115A Id, N-Channel MOSFET, SOT-23" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "SOT?23*" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "Transistor_FET:2N7002_0_1"
      (polyline
        (pts
          (xy 0.254 0)
          (xy -2.54 0)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.254 1.905)
          (xy 0.254 -1.905)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 -1.27)
          (xy 0.762 -2.286)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 0.508)
          (xy 0.762 -0.508)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 2.286)
          (xy 0.762 1.27)
        )
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 2.54 2.54)
          (xy 2.54 1.778)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 2.54 -2.54)
          (xy 2.54 0)
          (xy 0.762 0)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 0.762 -1.778)
          (xy 3.302 -1.778)
          (xy 3.302 1.778)
          (xy 0.762 1.778)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 1.016 0)
          (xy 2.032 0.381)
          (xy 2.032 -0.381)
          (xy 1.016 0)
        )
        (stroke (width 0) (type default))
        (fill (type outline))
      )
      (polyline
        (pts
          (xy 2.794 0.508)
          (xy 2.921 0.381)
          (xy 3.683 0.381)
          (xy 3.81 0.254)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (polyline
        (pts
          (xy 3.302 0.381)
          (xy 2.921 -0.254)
          (xy 3.683 -0.254)
          (xy 3.302 0.381)
        )
        (stroke (width 0) (type default))
        (fill (type none))
      )
      (circle (center 1.651 0) (radius 2.794)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
      (circle (center 2.54 -1.778) (radius 0.254)
        (stroke (width 0) (type default))
        (fill (type outline))
      )
      (circle (center 2.54 1.778) (radius 0.254)
        (stroke (width 0) (type default))
        (fill (type outline))
      )
    )
    (symbol "Transistor_FET:2N7002_1_1"
      (pin input line (at -5.08 0 0) (length 2.54)
        (name "G" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 2.54 -5.08 90) (length 2.54)
        (name "S" (effects (font (size 1.27 1.27))))
        (number "2" (effects (font (size 1.27 1.27))))
      )
      (pin passive line (at 2.54 5.08 270) (length 2.54)
        (name "D" (effects (font (size 1.27 1.27))))
        (number "3" (effects (font (size 1.27 1.27))))
      )
    )
  )'''

# ============================================================
# Generate components for the schematic
# ============================================================

def make_symbol_inst(comp_path, lib_id, ref, value, at_pos, rot=0):
    """Generate a (symbol ...) placement entry."""
    u = uid()
    at_x, at_y = at_pos
    mirror = ''
    
    # Different positioning for different component types
    if lib_id.startswith('Device:R'):
        fields = f'''(property "Reference" "{ref}" (at {at_x+2.032} {at_y} 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{value}" (at {at_x} {at_y} 90)
      (effects (font (size 1.27 1.27)))
    )'''
    elif lib_id.startswith('Device:C'):
        fields = f'''(property "Reference" "{ref}" (at {at_x+0.635} {at_y+2.54} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {at_x+0.635} {at_y-2.54} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )'''
    elif lib_id.startswith('power:'):
        fields = f'''(property "Reference" "#PWR" (at {at_x} {at_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "{value}" (at {at_x+0.5} {at_y+2.54} 0)
      (effects (font (size 1.27 1.27)))
    )'''
    elif lib_id.startswith('Amplifier_Operational:'):
        fields = f'''(property "Reference" "{ref}" (at {at_x} {at_y+5.08} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {at_x} {at_y-5.08} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )'''
    elif lib_id.startswith('Transistor_BJT') or lib_id.startswith('Transistor_FET'):
        fields = f'''(property "Reference" "{ref}" (at {at_x+5.08} {at_y+1.905} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {at_x+5.08} {at_y} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )'''
    else:
        fields = f'''(property "Reference" "{ref}" (at {at_x} {at_y} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "{value}" (at {at_x} {at_y} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )'''
    
    inst = f'''  (symbol (lib_id "{lib_id}") (at {at_x} {at_y} {rot}) (unit 1)
    (in_bom yes) (on_board yes)
    (uuid "{u}")
    {fields}
    (property "Datasheet" "~" (at {at_x} {at_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )'''
    return inst, u

# Layout coordinates (A4 portrait: 210x297mm, working area ~10-200mm X, 10-280mm Y)
# Section 1: HRPWM Input Filter + Voltage Divider (Y: 15-40)
# Section 2: Op-Amp + Push-Pull Driver (Y: 50-85)  
# Section 3: MOSFET Group 1 (Q3-Q8) (Y: 100-160)
# Section 4: MOSFET Group 2 (Q9-Q14) (Y: 175-235)
# Section 5: Protection MOSFETs (Y: 245-260)

components = []
symbol_instances = []

# --- Section 1: HRPWM Input ---
# R1 (10k) at X=30, Y=15
inst, u = make_symbol_inst('', 'Device:R', 'R1', '10kΩ', (30, 15))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "R1") (unit 1))')

# C1 (1uF) at X=60, Y=15
inst, u = make_symbol_inst('', 'Device:C', 'C1', '1μF', (60, 15))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "C1") (unit 1))')

# R2 (95k) at X=30, Y=35
inst, u = make_symbol_inst('', 'Device:R', 'R2', '95kΩ', (30, 35))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "R2") (unit 1))')

# R3 (5.23k) at X=60, Y=35
inst, u = make_symbol_inst('', 'Device:R', 'R3', '5.23kΩ', (60, 35))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "R3") (unit 1))')

# GND symbols for C1, R3
inst, u = make_symbol_inst('', 'power:GND', '#PWR01', 'GND', (60, 23))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR01") (unit 1))')

inst, u = make_symbol_inst('', 'power:GND', '#PWR02', 'GND', (60, 43))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR02") (unit 1))')

# --- Section 2: Op-Amp ---
# U1 (RS6332/LM358) at X=55, Y=60
inst, u = make_symbol_inst('', 'Amplifier_Operational:LM358', 'U1', 'RS6332', (55, 60))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "U1") (unit 1))')
# Need to add unit 2 for the second op-amp in the package
# Actually RS6332 is single op-amp, not dual. But LM358 is dual.
# Let me just use unit 1 for now.

# +5V and GND for U1
inst, u = make_symbol_inst('', 'power:+5V', '#PWR03', '+5V', (55, 52))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR03") (unit 1))')

inst, u = make_symbol_inst('', 'power:GND', '#PWR04', 'GND', (55, 68))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR04") (unit 1))')

# --- Section 2b: Push-Pull Driver ---
# R4 (220Ω NPN base) at X=35, Y=85
inst, u = make_symbol_inst('', 'Device:R', 'R4', '220Ω', (35, 85))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "R4") (unit 1))')

# R5 (220Ω PNP base) at X=55, Y=85
inst, u = make_symbol_inst('', 'Device:R', 'R5', '220Ω', (55, 85))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "R5") (unit 1))')

# Q1 D882 NPN at X=35, Y=100
inst, u = make_symbol_inst('', 'Transistor_BJT:D882', 'Q1', 'D882', (35, 100))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "Q1") (unit 1))')

# Q2 B772 PNP at X=65, Y=100
inst, u = make_symbol_inst('', 'Transistor_BJT:B772', 'Q2', 'B772', (65, 100))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "Q2") (unit 1))')

# +15V for Q1 collector, GND for Q2 collector
inst, u = make_symbol_inst('', 'power:+15V', '#PWR05', '+15V', (35, 93))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR05") (unit 1))')

inst, u = make_symbol_inst('', 'power:GND', '#PWR06', 'GND', (65, 108))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR06") (unit 1))')

# --- Section 3: MOSFET Group 1 (Q3-Q8, 6 MOSFETs) ---
# Y=130 for this group
# Place horizontally
mos_x_positions_g1 = [15, 45, 75, 105, 135, 165]
gate_drv_x = 90  # center

for i, mx in enumerate(mos_x_positions_g1):
    idx = i + 3  # Q3..Q8
    
    # MOSFET
    inst, u = make_symbol_inst('', 'Transistor_FET:M90N20', f'Q{idx}', 'M90N20', (mx, 130))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "Q{idx}") (unit 1))')
    
    # Gate resistor R_Gx (10Ω)
    rx = mx + 7
    inst, u = make_symbol_inst('', 'Device:R', f'RG{idx}', '10Ω', (rx, 118))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RG{idx}") (unit 1))')
    
    # Gate pull-down R_PDx (10kΩ)
    inst, u = make_symbol_inst('', 'Device:R', f'RPD{idx}', '10kΩ', (rx, 142))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RPD{idx}") (unit 1))')
    
    # Sense resistor R_Sx (0.05Ω)
    sy = 155
    inst, u = make_symbol_inst('', 'Device:R', f'RS{idx}', '0.05Ω', (mx, sy))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RS{idx}") (unit 1))')
    
    # Summing resistor R_SUMx (10kΩ)
    inst, u = make_symbol_inst('', 'Device:R', f'RSUM{idx}', '10kΩ', (mx, 170))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RSUM{idx}") (unit 1))')

# --- Section 4: MOSFET Group 2 (Q9-Q14, 6 MOSFETs) ---
# Y=200 for this group
mos_x_positions_g2 = [15, 45, 75, 105, 135, 165]

for i, mx in enumerate(mos_x_positions_g2):
    idx = i + 9  # Q9..Q14
    
    # MOSFET
    inst, u = make_symbol_inst('', 'Transistor_FET:M90N20', f'Q{idx}', 'M90N20', (mx, 200))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "Q{idx}") (unit 1))')
    
    # Gate resistor R_Gx (10Ω)
    rx = mx + 7
    inst, u = make_symbol_inst('', 'Device:R', f'RG{idx}', '10Ω', (rx, 188))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RG{idx}") (unit 1))')
    
    # Gate pull-down R_PDx (10kΩ)
    inst, u = make_symbol_inst('', 'Device:R', f'RPD{idx}', '10kΩ', (rx, 212))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RPD{idx}") (unit 1))')
    
    # Sense resistor R_Sx (0.05Ω)
    inst, u = make_symbol_inst('', 'Device:R', f'RS{idx}', '0.05Ω', (mx, 225))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RS{idx}") (unit 1))')
    
    # Summing resistor R_SUMx (10kΩ)
    inst, u = make_symbol_inst('', 'Device:R', f'RSUM{idx}', '10kΩ', (mx, 240))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "RSUM{idx}") (unit 1))')

# --- Section 5: Protection MOSFETs ---
# 2N7002 protection MOSFETs for gate pull-down on fault
# Q15-Q26, one per main MOSFET, placed near each
# Actually, let me add a few representative 2N7002 protection MOSFETs
# Q15-Q26 protection
for i in range(12):
    idx = i + 15
    # Place near each main MOSFET's gate connection
    gx = mos_x_positions_g1[i] if i < 6 else mos_x_positions_g2[i-6]
    gy = 145 if i < 6 else 215
    inst, u = make_symbol_inst('', 'Transistor_FET:2N7002', f'Q{idx}', '2N7002', (gx - 10, gy))
    components.append(inst)
    symbol_instances.append(f'    (path "/{u}" (reference "Q{idx}") (unit 1))')

# Now generate wires and net labels
# This is the complex part - let me generate the key connections

wires = []
labels = []

# Helper to add a wire
def add_wire(x1, y1, x2, y2):
    u = uid()
    wires.append(f'''  (wire (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{u}")
  )''')

# Helper to add a label
def add_label(text, x, y, angle=0, shape=''):
    u = uid()
    sh = f' (shape {shape})' if shape else ''
    angle_map = {0: 0, 90: 1, 180: 2, 270: 3}
    a = angle_map.get(angle, 0)
    labels.append(f'''  (label "{text}" (at {x} {y} {a}){sh}
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{u}")
  )''')

# === SECTION 1: HRPWM Input ===
# HRPWM_IN -> R1(1) 
add_wire(15, 15, 28.73, 15)  # from left edge to R1 pin 1
add_label('HRPWM_IN', 15, 15, 0)

# R1(2) -> C1(1) -> R2(1)
add_wire(31.27, 15, 58.73, 15)  # R1 pin 2 to C1 pin 1
add_wire(31.27, 15, 28.73, 35)  # R1 pin 2 to R2 pin 1

# C1(2) -> GND
add_wire(60, 18.81, 60, 23)  # C1 pin 2 to GND

# R2(2) -> R3(1)
add_wire(31.27, 35, 58.73, 35)  # R2 pin 2 to R3 pin 1

# R3(2) -> GND
add_wire(60, 38.81, 60, 43)  # R3 pin 2 to GND

# Voltage divider output = V_REF
add_label('V_REF', 45, 35, 90)

# V_REF -> U1 (non-inverting input, pin 3)
add_wire(45, 35, 45, 55)
add_wire(45, 55, 47.46, 55)

# === SECTION 2: Op-Amp ===
# U1 pin 1 (OUT) -> gate driver
add_wire(62.54, 60, 75, 60)
add_wire(75, 60, 75, 75)
add_wire(75, 75, 38, 75)
add_label('OPAMP_OUT', 75, 60, 0)

# OPAMP_OUT -> R4(1) and R5(1)
add_wire(38, 75, 33.73, 85)  # to R4 pin 1
add_wire(38, 75, 53.73, 85)  # to R5 pin 1

# U1 pin 8 (V+) -> +5V
add_wire(55, 52.38, 55, 52)

# U1 pin 4 (V-) -> GND
add_wire(55, 67.62, 55, 68)

# U1 pin 2 (IN-) -> summing node
add_label('SUMMING_NODE', 35, 60, 180)

# === Push-Pull Drive ===
# R4(2) -> Q1 B (pin 2)
add_wire(36.27, 85, 38, 88)
add_wire(38, 88, 29.285, 100)  # to Q1 base

# R5(2) -> Q2 B (pin 2)
add_wire(56.27, 85, 58, 88)
add_wire(58, 88, 59.285, 100)  # to Q2 base

# Q1 E (pin 1) -> Q2 E (pin 1) -> GATE_DRV
add_wire(37.54, 95.08, 37.54, 90)
add_wire(37.54, 90, 67.54, 90)
add_wire(67.54, 90, 67.54, 95.08)
add_label('GATE_DRV', 50, 90, 0)

# Q1 C (pin 3) -> +15V
add_wire(37.54, 105.08, 37.54, 93)

# Q2 C (pin 3) -> GND
add_wire(67.54, 105.08, 67.54, 108)

# === Section 3 & 4: GATE_DRV to all gate resistors ===
# Horizontal bus
add_wire(50, 90, 50, 92)

# GATE_DRV bus to Group 1 gate resistors
for i, mx in enumerate(mos_x_positions_g1):
    idx = i + 3
    rx = mx + 7
    # From GATE_DRV bus down to each gate resistor top
    gx = mx + 3
    add_wire(rx, 90, rx, 116.73)
    # Resistor bottom to MOSFET gate (pin 1)
    add_wire(rx, 119.27, mx, 127.46)

# GATE_DRV bus to Group 2 gate resistors
for i, mx in enumerate(mos_x_positions_g2):
    idx = i + 9
    rx = mx + 7
    gx = mx + 3
    add_wire(rx, 92, rx, 116.73)  # wrong Y, needs fixing - group 2 is at Y=200
    # Actually the gate drive line needs to run down further
    # Let me fix this - I'll add a vertical bus line

# Remove the previous incorrect wires and redo properly
# Clear and regenerate properly
wires = []
labels = []

# === REDO WIRES PROPERLY ===

# SECTION 1: HRPWM Input
add_wire(15, 15, 28.73, 15)
add_label('HRPWM_IN', 10, 15, 0)
add_wire(31.27, 15, 58.73, 15)
add_wire(31.27, 15, 28.73, 35)
add_wire(60, 18.81, 60, 23)
add_wire(31.27, 35, 58.73, 35)
add_wire(60, 38.81, 60, 43)
add_label('V_REF', 45, 32, 90)
add_wire(45, 35, 45, 57.46)
add_wire(60, 23, 60, 43)

# SECTION 2: Op-Amp + Push-Pull
add_wire(47.46, 60, 62.54, 60)
add_label('OPAMP_OUT', 65, 58, 0)

add_wire(62.54, 60, 75, 60)
add_wire(75, 60, 75, 80)
add_wire(75, 80, 33.73, 80)  # horizontal to R4/R5
add_wire(33.73, 80, 33.73, 83.73)  # down to R4 pin 1
add_wire(53.73, 80, 53.73, 83.73)  # down to R5 pin 1

# U1 power
add_wire(55, 52.38, 55, 52)
add_wire(55, 67.62, 55, 68)

# Summing node label
add_label('SUMMING_NODE', 30, 63, 180)
# Connection from U1 pin 2 to summing node - through right side
# Actually pin 2 is on the left side of the op-amp at (-7.62, -2.54) relative to center (55,60)
# So that's at (47.38, 57.46)
add_wire(47.38, 57.46, 40, 57.46)
add_wire(40, 57.46, 40, 63)

# R4(2) -> Q1 base (B pin 2 at -5.08,0 relative to (35,100) = 29.92,100)
add_wire(35, 88.73, 35, 93)
add_wire(35, 93, 29.92, 93)
add_wire(29.92, 93, 29.92, 100)

# R5(2) -> Q2 base (B pin 2 at -5.08,0 relative to (65,100) = 59.92,100)
add_wire(55, 88.73, 55, 93)
add_wire(55, 93, 59.92, 93)
add_wire(59.92, 93, 59.92, 100)

# Q1 E (pin 1 at 2.54,-5.08 relative to (35,100) = 37.54,94.92)
# Q2 E (pin 1 at 2.54,-5.08 relative to (65,100) = 67.54,94.92)
add_wire(37.54, 94.92, 37.54, 88)
add_wire(37.54, 88, 67.54, 88)
add_wire(67.54, 94.92, 67.54, 88)
add_label('GATE_DRV', 50, 86, 0)

# Q1 C (pin 3 at 2.54,5.08 relative to (35,100) = 37.54,105.08) -> +15V
add_wire(37.54, 105.08, 37.54, 93)

# Q2 C (pin 3 at 2.54,5.08 relative to (65,100) = 67.54,105.08) -> GND
add_wire(67.54, 105.08, 67.54, 108)

# GATE_DRV vertical bus down
add_wire(50, 88, 50, 125)  # down to Group 1
add_wire(50, 125, 50, 195)  # down to Group 2

# Group 1 MOSFETs (Q3-Q8, Y=130)
g1_gate_y = 125  # horizontal gate bus Y
g1_mos_y = 130

for i, mx in enumerate(mos_x_positions_g1):
    idx = i + 3
    rx = mx + 7  # gate resistor X
    
    # GATE_DRV bus to gate resistor (pin 1, top)
    add_wire(50, g1_gate_y, rx, g1_gate_y)
    add_wire(rx, g1_gate_y, rx, 126.73)
    
    # Gate resistor (pin 2, bottom) to MOSFET gate (G, pin 1 at -5.08,0 rel = mx-5.08,130)
    add_wire(rx, 129.27, mx-5.08, 130)
    
    # Gate pull-down: between gate and source
    # RPD top (pin 1) connected to gate
    # RPD at (rx, 142), pin 1 at top (y=138.19), pin 2 at bottom (y=145.81)
    add_wire(mx-5.08, 130, rx, 138.19)  # gate to RPD top
    
    # RPD bottom to MOSFET source (S, pin 3 at 2.54,-5.08 rel = mx+2.54,124.92)
    # Actually S is at bottom: 2.54,-5.08 relative to (mx,130) = mx+2.54, 124.92
    # Wait, S is pin 3 at (2.54, -5.08) relative to center
    # That means it's at X=mx+2.54, Y=130-5.08=124.92
    add_wire(rx, 145.81, mx+2.54, 124.92)  # RPD bottom to source
    
    # Sense resistor RS at (mx, 155)
    # RS pin 1 (top) at (mx, 151.19), RS pin 2 (bottom) at (mx, 158.81)
    # MOSFET source to RS top
    add_wire(mx+2.54, 124.92, mx, 151.19)
    
    # Summing resistor RSUM at (mx, 170)
    # RSUM pin 1 (top) at (mx, 166.19), RSUM pin 2 (bottom) at (mx, 173.81)
    # Source tap to RSUM top
    add_wire(mx+2.54, 124.92, mx, 166.19)

# Group 2 MOSFETs (Q9-Q14, Y=200)
g2_mos_y = 200
g2_gate_y = 195

for i, mx in enumerate(mos_x_positions_g2):
    idx = i + 9
    rx = mx + 7  # gate resistor X
    
    # GATE_DRV bus to gate resistor (pin 1, top)
    add_wire(50, g2_gate_y, rx, g2_gate_y)
    add_wire(rx, g2_gate_y, rx, 196.73)
    
    # Gate resistor (pin 2, bottom) to MOSFET gate
    add_wire(rx, 199.27, mx-5.08, 200)
    
    # Gate pull-down
    # RPD at (rx, 212), pin 1 at y=208.19, pin 2 at y=215.81
    add_wire(mx-5.08, 200, rx, 208.19)
    add_wire(rx, 215.81, mx+2.54, 194.92)
    
    # Sense resistor RS at (mx, 225)
    add_wire(mx+2.54, 194.92, mx, 221.19)
    
    # Summing resistor
    add_wire(mx+2.54, 194.92, mx, 236.19)

# Summing resistors all connect to SUMMING_NODE
# Horizontal summing bus
sum_bus_y = 63
# Group 1
for i, mx in enumerate(mos_x_positions_g1):
    rx = mx + 7
    # RSUM (pin 2, bottom) -> summing bus
    # RSUM at (mx, 170), pin 2 at (mx, 173.81), go up to summing bus
    # Actually, summing resistors go from source tap to op-amp IN-
    # Source tap is at mx+2.54, 124.92
    # RSUM bottom connects to summing bus, top to source
    # Let me connect RSUM bottom (mx, 173.81) to summing bus
    add_wire(mx, 173.81, mx, sum_bus_y)  # vertical to summing bus

# Group 2
for i, mx in enumerate(mos_x_positions_g2):
    rx = mx + 7
    add_wire(mx, 243.81, mx, sum_bus_y)

# Horizontal summing bus line connecting all summing resistors and op-amp IN-
# Need horizontal lines between the vertical wires
sorted_x = sorted(set(mos_x_positions_g1 + mos_x_positions_g2))
for i in range(len(sorted_x)-1):
    add_wire(sorted_x[i], sum_bus_y, sorted_x[i+1], sum_bus_y)

# Connection from summing bus to U1 pin 2
# U1 pin 2 is at (-7.62, -2.54) relative to (55, 60) = (47.38, 57.46)
# Summing bus is at Y=63, rightmost is at X=165
# Connect from summing bus right side to U1 pin 2
add_wire(15, sum_bus_y, 40, sum_bus_y)
add_wire(40, sum_bus_y, 40, 57.46)
add_wire(40, 57.46, 47.38, 57.46)

# LOAD+ (drain bus) - all drains connect together
# MOSFET D (pin 2 at 2.54,5.08 relative to center) = mx+2.54, 135.08 for G1, mx+2.54, 205.08 for G2
drain_bus_y_g1 = 135.08
drain_bus_y_g2 = 205.08
drain_bus_x = 180

for i, mx in enumerate(mos_x_positions_g1):
    add_wire(mx+2.54, 135.08, drain_bus_x, 135.08)

for i, mx in enumerate(mos_x_positions_g2):
    add_wire(mx+2.54, 205.08, drain_bus_x, 205.08)

# Connect the two drain buses
add_wire(drain_bus_x, 135.08, drain_bus_x, 205.08)
add_label('LOAD+', drain_bus_x+2, 170, 90)

# LOAD- (sense resistor bottoms) - all connect to GND
# RS pin 2 at (mx, 158.81) for G1, (mx, 228.81) for G2
gnd_bus_x = 190

for mx in mos_x_positions_g1:
    add_wire(mx, 158.81, gnd_bus_x, 158.81)

for mx in mos_x_positions_g2:
    add_wire(mx, 228.81, gnd_bus_x, 228.81)

# Connect the two GND buses and add GND symbol
add_wire(gnd_bus_x, 158.81, gnd_bus_x, 228.81)
add_label('GND', gnd_bus_x+2, 195, 90)

# Add GND power symbol for load ground
inst, u = make_symbol_inst('', 'power:GND', '#PWR07', 'GND', (gnd_bus_x, 195))
components.append(inst)
symbol_instances.append(f'    (path "/{u}" (reference "#PWR07") (unit 1))')
add_wire(gnd_bus_x, 195, gnd_bus_x, 195)

# Add +5V power label
add_label('+5V', 55, 50, 90)

# Add +15V power label
add_label('+15V', 35, 91, 90)

# Text annotations
text_annotations = [
    (10, 10, 'EL-1000 Power Stage v0.4'),
    (10, 5, 'HRPWM RC Filter: R1(10kΩ) + C1(1μF) = 15.2-bit effective DAC'),
    (10, 30, 'Voltage Divider: R2(95kΩ) + R3(5.23kΩ) = 1/19.17 ratio'),
    (10, 55, 'RS6332 Op-Amp (SOIC-8, LM358-compatible)'),
    (10, 80, 'Push-Pull Gate Driver: D882(NPN) + B772(PNP)'),
    (10, 118, 'MOSFET Group 1: Q3-Q8 M90N20 (TO-247)'),
    (10, 188, 'MOSFET Group 2: Q9-Q14 M90N20 (TO-247)'),
]

text_entries = []
for tx, ty, ttext in text_annotations:
    tu = uid()
    text_entries.append(f'''  (text "{ttext}" (at {tx} {ty} 0)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{tu}")
  )''')

# ============================================================
# Assemble the full .kicad_sch file
# ============================================================

lib_symbols = [
    SYM_R, SYM_C, SYM_GND, SYM_5V, SYM_15V,
    SYM_LM358, SYM_NPN, SYM_PNP, SYM_NMOS, SYM_NMOS_PROT
]

# Title block
title_block = '''    (title_block
      (title "EL-1000 Power Stage")
      (date "2026-05-30")
      (rev "0.4")
      (company "CCS Electronics")
      (comment 1 "1000W Electronic Load - Power Stage v0.4")
      (comment 2 "HRPWM + Op-Amp + Push-Pull + 12x M90N20 MOSFETs")
    )'''

sch_uuid = uid()

schematic_lines = [
    f'(kicad_sch (version 20230121) (generator eeschema)',
    f'  (uuid "{sch_uuid}")',
    f'  (paper "A4" portrait)',
    title_block,
    f'  (lib_symbols',
]

for sym in lib_symbols:
    schematic_lines.append(sym)

schematic_lines.append('  )')
schematic_lines.append('')

# Add components
for comp in components:
    schematic_lines.append(comp)

schematic_lines.append('')

# Add wires
for w in wires:
    schematic_lines.append(w)

schematic_lines.append('')

# Add labels
for l in labels:
    schematic_lines.append(l)

schematic_lines.append('')

# Add text annotations
for t in text_entries:
    schematic_lines.append(t)

schematic_lines.append('')

# Sheet instances
schematic_lines.append('  (sheet_instances')
schematic_lines.append('    (path "/" (page "1"))')
schematic_lines.append('  )')
schematic_lines.append('')

# Symbol instances
schematic_lines.append('  (symbol_instances')
for si in symbol_instances:
    schematic_lines.append(si)
schematic_lines.append('  )')

schematic_lines.append(')')

with open('/home/hermes/EL-1000_PowerStage.kicad_sch', 'w') as f:
    f.write('\n'.join(schematic_lines))
    f.write('\n')

print("Schematic written successfully!")
print(f"Total lines: {len(schematic_lines)}")
print(f"Components: {len(components)}")
print(f"Wires: {len(wires)}")
print(f"Labels: {len(labels)}")
print(f"Symbol instances: {len(symbol_instances)}")
