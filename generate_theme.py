#!/usr/bin/env python3
"""
HUGINN Terminal Theme Generator
Cyberpunk + Norse mythology inspired terminal theme for macOS Terminal.app
"""

import plistlib
import subprocess
import sys

# Try PyObjC (system Python on macOS has it)
try:
    from AppKit import NSColor, NSFont, NSKeyedArchiver, NSCalibratedRGBColorSpace
    HAS_PYOBJC = True
except ImportError:
    HAS_PYOBJC = False


def color_to_data(r, g, b, a=1.0):
    """Convert RGBA floats (0-1) to NSKeyedArchiver data."""
    if HAS_PYOBJC:
        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
        return NSKeyedArchiver.archivedDataWithRootObject_(color).bytes()
    else:
        # Fallback: manually construct the NSKeyedArchiver binary plist
        # This creates a minimal NSKeyedArchiver for NSColor
        return _manual_color_archive(r, g, b, a)


def font_to_data(name, size):
    """Convert font name + size to NSKeyedArchiver data."""
    if HAS_PYOBJC:
        font = NSFont.fontWithName_size_(name, size)
        if font is None:
            font = NSFont.fontWithName_size_("Menlo-Regular", size)
        return NSKeyedArchiver.archivedDataWithRootObject_(font).bytes()
    else:
        return _manual_font_archive(name, size)


def _manual_color_archive(r, g, b, a):
    """Manually construct NSKeyedArchiver data for an NSColor (calibrated RGB)."""
    import struct

    # We'll use the textual NSColor archiving format instead
    # NSColor stores as: float float float float (RGBA) in calibrated RGB space
    color_string = f"{r} {g} {b} {a}"

    plist = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "$class": plistlib.UID(2),
                "NSColorSpace": 1,  # NSCalibratedRGBColorSpace
                "NSRGB": color_string.encode("ascii"),
            },
            {
                "$classname": "NSColor",
                "$classes": ["NSColor", "NSObject"],
            },
        ],
    }
    return plistlib.dumps(plist, fmt=plistlib.FMT_BINARY)


def _manual_font_archive(name, size):
    """Manually construct NSKeyedArchiver data for an NSFont."""
    plist = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "$class": plistlib.UID(2),
                "NSName": plistlib.UID(3),
                "NSSize": float(size),
                "NSfFlags": 16,
            },
            {
                "$classname": "NSFont",
                "$classes": ["NSFont", "NSObject"],
            },
            name,
        ],
    }
    return plistlib.dumps(plist, fmt=plistlib.FMT_BINARY)


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB floats (0-1)."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


# ============================================================
# HUGINN COLOR PALETTE
# Cyberpunk darkness meets Norse mythology gold
# ============================================================

COLORS = {
    # Main colors
    "background":    "#080c12",   # Deep void black with blue undertone (Ginnungagap)
    "foreground":    "#b0c4de",   # Light steel blue (rune inscription color)
    "bold":          "#00e5ff",   # Neon cyan (cyberpunk highlight)
    "cursor":        "#ffc107",   # Amber gold (Odin's eye / HUGINN's gaze)
    "selection":     "#1a2744",   # Dark midnight blue (subtle selection)

    # ANSI Normal
    "black":         "#0d1117",   # Near black
    "red":           "#ff003c",   # Neon red (Ragnarok fire)
    "green":         "#00ff9f",   # Neon mint (Yggdrasil leaves)
    "yellow":        "#ffc107",   # Amber gold (Odin's treasure)
    "blue":          "#0080ff",   # Electric blue (Bifrost bridge)
    "magenta":       "#d946ef",   # Neon purple (Seidr magic)
    "cyan":          "#00e5ff",   # Bright cyan (frost giant ice)
    "white":         "#b0c4de",   # Light steel blue

    # ANSI Bright
    "bright_black":  "#2a3040",   # Dark grey (shadow realm)
    "bright_red":    "#ff5577",   # Soft neon red
    "bright_green":  "#66ffcc",   # Bright mint
    "bright_yellow": "#ffe066",   # Bright gold
    "bright_blue":   "#5cadff",   # Sky blue
    "bright_magenta":"#e879f9",   # Bright purple
    "bright_cyan":   "#67e8f9",   # Light cyan
    "bright_white":  "#f0f4fc",   # Almost white (moonlight)
}


def build_profile():
    """Build the complete Terminal.app profile dictionary."""
    profile = {}

    # Profile metadata
    profile["name"] = "HUGINN"
    profile["type"] = "Window Settings"

    # Font — MesloLGS NF if available, otherwise Menlo
    profile["Font"] = font_to_data("MesloLGS-NF-Regular", 13.0)

    # Main colors
    r, g, b = hex_to_rgb(COLORS["background"])
    profile["BackgroundColor"] = color_to_data(r, g, b, 0.95)  # slight transparency

    r, g, b = hex_to_rgb(COLORS["foreground"])
    profile["TextColor"] = color_to_data(r, g, b)

    r, g, b = hex_to_rgb(COLORS["bold"])
    profile["TextBoldColor"] = color_to_data(r, g, b)

    r, g, b = hex_to_rgb(COLORS["cursor"])
    profile["CursorColor"] = color_to_data(r, g, b)

    r, g, b = hex_to_rgb(COLORS["selection"])
    profile["SelectionColor"] = color_to_data(r, g, b, 0.85)

    # ANSI colors (order matters: black, red, green, yellow, blue, magenta, cyan, white)
    ansi_normal = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    ansi_bright = [f"bright_{c}" for c in ansi_normal]

    for i, name in enumerate(ansi_normal):
        r, g, b = hex_to_rgb(COLORS[name])
        profile[f"ANSIColor{i}"] = color_to_data(r, g, b)  # Added key name fix

    for i, name in enumerate(ansi_bright):
        r, g, b = hex_to_rgb(COLORS[name])
        profile[f"ANSIBrightColor{i}"] = color_to_data(r, g, b)

    # Wait, Terminal.app uses different key names. Let me fix this.
    # The correct keys are:
    # ANSIBlackColor, ANSIRedColor, etc. for normal
    # ANSIBrightBlackColor, ANSIBrightRedColor, etc. for bright

    # Remove the wrong keys and add correct ones
    for i in range(8):
        profile.pop(f"ANSIColor{i}", None)
        profile.pop(f"ANSIBrightColor{i}", None)

    ansi_key_names = [
        "ANSIBlackColor", "ANSIRedColor", "ANSIGreenColor", "ANSIYellowColor",
        "ANSIBlueColor", "ANSIMagentaColor", "ANSICyanColor", "ANSIWhiteColor",
    ]
    ansi_bright_key_names = [
        "ANSIBrightBlackColor", "ANSIBrightRedColor", "ANSIBrightGreenColor",
        "ANSIBrightYellowColor", "ANSIBrightBlueColor", "ANSIBrightMagentaColor",
        "ANSIBrightCyanColor", "ANSIBrightWhiteColor",
    ]

    for key, name in zip(ansi_key_names, ansi_normal):
        r, g, b = hex_to_rgb(COLORS[name])
        profile[key] = color_to_data(r, g, b)

    for key, name in zip(ansi_bright_key_names, ansi_bright):
        r, g, b = hex_to_rgb(COLORS[name])
        profile[key] = color_to_data(r, g, b)

    # Window settings
    profile["columnCount"] = 120
    profile["rowCount"] = 35

    # Cursor style: 0=block, 1=underline, 2=vertical bar
    profile["CursorType"] = 0  # Block cursor — solid, like a rune
    profile["CursorBlink"] = True

    # Background blur & transparency
    profile["BackgroundBlur"] = 0.15
    profile["BackgroundAlphaInactive"] = 0.92
    profile["BackgroundSettingsForInactiveWindows"] = True

    # Visual bell instead of audible
    profile["VisualBell"] = True
    profile["VisualBellOnlyWhenMuted"] = False
    profile["Bell"] = False

    # Scrollback
    profile["ScrollbackLines"] = 10000

    # Shell
    profile["shellExitAction"] = 1  # Close if clean exit

    # Use bold fonts
    profile["UseBoldFonts"] = True

    # Disable ANSI colors override
    profile["UseANSIColors"] = True  # Added missing key

    return profile


def main():
    profile = build_profile()

    output_path = "/Users/karlogb/Desktop/terminal_theme/HUGINN.terminal"
    with open(output_path, "wb") as f:
        plistlib.dump(profile, f, fmt=plistlib.FMT_XML)

    print(f"Theme generated: {output_path}")
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║           H U G I N N                    ║")
    print("  ║     Odin's Raven Terminal Theme          ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  Background:  #080c12  (Ginnungagap)    ║")
    print("  ║  Text:        #b0c4de  (Rune Silver)    ║")
    print("  ║  Bold:        #00e5ff  (Frost Cyan)     ║")
    print("  ║  Cursor:      #ffc107  (Odin's Eye)     ║")
    print("  ║  Red:         #ff003c  (Ragnarok)       ║")
    print("  ║  Green:       #00ff9f  (Yggdrasil)      ║")
    print("  ║  Blue:        #0080ff  (Bifrost)        ║")
    print("  ║  Magenta:     #d946ef  (Seidr Magic)    ║")
    print("  ║  Yellow:      #ffc107  (Odin's Gold)    ║")
    print("  ║  Cyan:        #00e5ff  (Frost Giant)    ║")
    print("  ╚══════════════════════════════════════════╝")
    print()
    print("  Install: double-click HUGINN.terminal")
    print("  Then set as default in Terminal > Settings > Profiles")


if __name__ == "__main__":
    main()
