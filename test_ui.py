from machine import UART
import utime
from utils.minitel_ui import (
    G0, G1,
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
    NORMAL_SIZE, DOUBLE_HEIGHT, DOUBLE_WIDTH, DOUBLE_SIZE,
    BLINK_ON, BLINK_OFF,
    move, fg, bg, draw_hline, draw_box, fill_row, write_centered,
    clear_screen, read_key,
)

# Switch Minitel from default 1200 baud to 4800 baud
ser = UART(0, 1200, bits=7, parity=2, stop=1)
ser.write(b'\x1B\x3A\x6B\x76')
utime.sleep_ms(300)
ser = UART(0, 4800, bits=7, parity=2, stop=1)


def wait_suite():
    """Wait for SUITE key (0x48) to advance to next test."""
    utime.sleep_ms(200)
    fill_row(ser, 24, YELLOW, BLACK)
    move(ser, 24, 1)
    bg(ser, YELLOW)
    fg(ser, BLACK)
    ser.write(" SUITE: test suivant ")
    while True:
        key = read_key(ser, timeout_ms=0)
        if key == 0x48:
            return


# ============================================================
# TEST 1: fg/bg order and basic colors
# ============================================================
# Expected:
#   Row 1:  "TEST 1: COULEURS" centered, white on black
#   Row 3:  cyan badge with black "A" text, then white "Titre" on black
#   Row 4:  same but fg BEFORE bg (may be broken on your Minitel)
#   Row 6:  "bg then fg" label in green
#   Row 7:  "fg then bg" label in green
#   Row 9:  8 color swatches (blocks) from black to white
#   Row 24: yellow bar "SUITE: test suivant"
# ============================================================
clear_screen(ser)
write_centered(ser, 1, "TEST 1: COULEURS")

# Test A: bg before fg (correct order per other pages)
move(ser, 3, 2)
bg(ser, CYAN)
fg(ser, BLACK)
ser.write(" A ")
bg(ser, BLACK)
fg(ser, WHITE)
ser.write(" Titre (bg puis fg)")

# Test B: fg before bg (reversed — may be broken)
move(ser, 4, 2)
fg(ser, BLACK)
bg(ser, CYAN)
ser.write(" B ")
bg(ser, BLACK)
fg(ser, WHITE)
ser.write(" Titre (fg puis bg)")

# Labels
move(ser, 6, 2)
bg(ser, BLACK)
fg(ser, GREEN)
ser.write("Row 3 = bg puis fg (ordre normal)")
move(ser, 7, 2)
fg(ser, GREEN)
ser.write("Row 4 = fg puis bg (ordre inverse)")

# Color swatches: show all 8 bg colors side by side
move(ser, 9, 2)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("Couleurs disponibles:")
move(ser, 10, 2)
colors = [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
names = ["NR", "RG", "VT", "JN", "BL", "MG", "CY", "BC"]
for c, name in zip(colors, names):
    bg(ser, c)
    if c == BLACK or c == BLUE:
        fg(ser, WHITE)
    else:
        fg(ser, BLACK)
    ser.write(" {} ".format(name))

# Color names below
move(ser, 12, 2)
bg(ser, BLACK)
fg(ser, CYAN)
ser.write("NR=noir RG=rouge VT=vert JN=jaune")
move(ser, 13, 2)
ser.write("BL=bleu MG=magenta CY=cyan BC=blanc")

wait_suite()


# ============================================================
# TEST 2: fill_row and draw_hline
# ============================================================
# Expected:
#   Row 1:  full magenta row with white "TEST 2" text
#   Row 3:  full blue row with yellow text
#   Row 5:  cyan mosaic horizontal line (full width)
#   Row 7:  cyan mosaic horizontal line (char 0x3F, denser)
#   Row 9:  "Lignes ok?" in white
#   Row 24: yellow bar
# ============================================================
clear_screen(ser)

fill_row(ser, 1, MAGENTA, WHITE)
move(ser, 1, 1)
bg(ser, MAGENTA)
fg(ser, WHITE)
ser.write(" TEST 2: FILL_ROW & DRAW_HLINE")

fill_row(ser, 3, BLUE, YELLOW)
move(ser, 3, 1)
bg(ser, BLUE)
fg(ser, YELLOW)
ser.write(" Ligne bleue avec texte jaune")

# Default hline char (0x23)
draw_hline(ser, 5, 1, 40)

# Denser hline char (0x3F) — used in actual pages
utime.sleep_ms(200)
draw_hline(ser, 7, 1, 40, 0x3F)

utime.sleep_ms(200)
move(ser, 9, 2)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("Row 5 = hline char 0x23 (defaut)")
move(ser, 10, 2)
ser.write("Row 7 = hline char 0x3F (dense)")
utime.sleep_ms(100)
move(ser, 12, 2)
fg(ser, CYAN)
ser.write("Les 2 lignes font 40 colonnes?")

wait_suite()


# ============================================================
# TEST 3: draw_box and write_centered
# ============================================================
# Expected:
#   Row 1:  "TEST 3" centered in white
#   Row 3-8: cyan box outline (16 cols wide, 6 rows tall)
#   Row 5:  "BONJOUR" centered inside the box
#   Row 10-15: another box (20 wide, 6 tall) in magenta
#   Row 12: "MINITEL" centered inside
#   Row 24: yellow bar
# ============================================================
clear_screen(ser)
write_centered(ser, 1, "TEST 3: BOX & CENTRAGE")

draw_box(ser, 3, 12, 16, 6, CYAN)
move(ser, 5, 16)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("BONJOUR")

draw_box(ser, 10, 10, 20, 6, MAGENTA)
move(ser, 12, 14)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("MINITEL 1")

wait_suite()


# ============================================================
# TEST 4: text sizes
# ============================================================
# Expected:
#   Row 1:  "TEST 4" in white
#   Row 3:  "Normal" in normal size
#   Row 5:  "Double H" in double height (occupies rows 4-5)
#   Row 8:  "Double W" in double width (chars are 2 cols wide)
#   Row 11: "Double" in double size (2x height + 2x width, rows 10-11)
#   Row 24: yellow bar
# ============================================================
clear_screen(ser)
write_centered(ser, 1, "TEST 4: TAILLES")

move(ser, 3, 2)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("Normal")

# Double height: text on row 5, top half extends to row 4
move(ser, 5, 2)
bg(ser, BLACK)
fg(ser, CYAN)
ser.write(DOUBLE_HEIGHT)
ser.write("Double H")
ser.write(NORMAL_SIZE)

# Double width
move(ser, 8, 2)
bg(ser, BLACK)
fg(ser, GREEN)
ser.write(DOUBLE_WIDTH)
ser.write("Double W")
ser.write(NORMAL_SIZE)

# Double size (height + width): text on row 11, top half on row 10
move(ser, 11, 2)
bg(ser, BLACK)
fg(ser, YELLOW)
ser.write(DOUBLE_SIZE)
ser.write("Double")
ser.write(NORMAL_SIZE)

move(ser, 14, 2)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("Toutes les tailles visibles?")

wait_suite()


# ============================================================
# TEST 5: blink
# ============================================================
# Expected:
#   Row 1:  "TEST 5" in white
#   Row 4:  "CLIGNOTANT" blinking in red
#   Row 6:  "STABLE" not blinking in green
#   Row 24: yellow bar
# ============================================================
clear_screen(ser)
write_centered(ser, 1, "TEST 5: CLIGNOTEMENT")

move(ser, 4, 2)
bg(ser, BLACK)
fg(ser, RED)
ser.write(BLINK_ON)
ser.write("CLIGNOTANT")
ser.write(BLINK_OFF)

move(ser, 6, 2)
bg(ser, BLACK)
fg(ser, GREEN)
ser.write("STABLE (pas de clignotement)")

wait_suite()


# ============================================================
# TEST 6: G1 mosaic mode
# ============================================================
# Expected:
#   Row 1:  "TEST 6" in white
#   Row 3:  row of mosaic chars 0x20 to 0x3F in cyan (G1 mode)
#   Row 4:  row of mosaic chars 0x40 to 0x5F in cyan (G1 mode)
#   Row 6:  "ABCDEF" in normal text (G0 mode) to confirm mode reset
#   Row 24: yellow bar
# ============================================================
clear_screen(ser)
write_centered(ser, 1, "TEST 6: MODE MOSAIQUE G1")

move(ser, 3, 2)
ser.write(G1)
bg(ser, BLACK)
fg(ser, CYAN)
for c in range(0x20, 0x40):
    ser.write(bytes([c]))

move(ser, 4, 2)
ser.write(G1)
fg(ser, CYAN)
for c in range(0x40, 0x60):
    ser.write(bytes([c]))
ser.write(G0)

move(ser, 6, 2)
bg(ser, BLACK)
fg(ser, WHITE)
ser.write("ABCDEF (retour mode texte G0)")

wait_suite()


# ============================================================
# DONE
# ============================================================
clear_screen(ser)
write_centered(ser, 10, "TESTS TERMINES")
move(ser, 12, 2)
bg(ser, BLACK)
fg(ser, GREEN)
write_centered(ser, 12, "Merci!")
