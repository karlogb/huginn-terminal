#!/bin/bash
# HUGINN Theme Color Test

echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║         H U G I N N  Color Test          ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

# Normal ANSI colors
echo "  ── Normal Colors ──"
echo -e "  \033[30m██ Black (Void)      \033[31m██ Red (Ragnarök)    \033[32m██ Green (Yggdrasil) \033[33m██ Yellow (Odin's Gold)\033[0m"
echo -e "  \033[34m██ Blue (Bifrost)    \033[35m██ Magenta (Seiðr)   \033[36m██ Cyan (Frost)      \033[37m██ White (Rune Silver)\033[0m"
echo ""

# Bright ANSI colors
echo "  ── Bright Colors ──"
echo -e "  \033[90m██ Bright Black      \033[91m██ Bright Red        \033[92m██ Bright Green      \033[93m██ Bright Yellow\033[0m"
echo -e "  \033[94m██ Bright Blue       \033[95m██ Bright Magenta    \033[96m██ Bright Cyan       \033[97m██ Bright White\033[0m"
echo ""

# Text styles
echo "  ── Text Styles ──"
echo -e "  \033[0mNormal text    \033[1mBold text (Frost Cyan)    \033[4mUnderlined    \033[0m"
echo ""

# Color bars (background blocks)
echo "  ── Full Palette ──"
for i in {0..7}; do
    echo -en "  \033[48;5;${i}m    \033[0m"
done
echo ""
for i in {8..15}; do
    echo -en "  \033[48;5;${i}m    \033[0m"
done
echo ""
echo ""

# Cursor
echo -e "  Cursor: \033[33m▊▊▊ (Odin's Eye - Amber Gold)\033[0m"
echo ""

# Sample real-world output
echo "  ── Sample Output ──"
echo -e "  \033[32m✓\033[0m Build successful     \033[34m→\033[0m Deploy to GCP"
echo -e "  \033[31m✗\033[0m 3 tests failed       \033[33m⚠\033[0m Fee not included"
echo -e "  \033[35m⟐\033[0m HUGINN v2.0.0        \033[36m◆\033[0m 15m candles active"
echo ""
