import utime
from utils.minitel_ui import (
    BLACK, CYAN, WHITE, BLUE, GREEN,
    NORMAL_SIZE, DOUBLE_HEIGHT,
    BLINK_ON, BLINK_OFF,
    move, fg, bg, draw_hline, fill_row, clear_screen,
)


def draw(ser):
    """Draw the main menu screen."""
    clear_screen(ser)

    # Title on row 2 so double-height top half extends into row 1
    fill_row(ser, 1, BLUE, WHITE)           # row 1
    fill_row(ser, 2, BLUE, WHITE)           # row 2
    move(ser, 2, 1)                         # row 2
    bg(ser, BLUE)                           # row 2
    fg(ser, WHITE)                          # row 2
    ser.write(DOUBLE_HEIGHT)                # row 2
    ser.write("  3615 PARIS INFO")          # row 2
    ser.write(NORMAL_SIZE)                  # row 2

    # Row 3 left empty for double-height title extension
    fill_row(ser, 3, BLUE, WHITE)           # row 3

    fill_row(ser, 4, BLUE, CYAN)            # row 4
    move(ser, 4, 1)                         # row 4
    bg(ser, BLUE)                           # row 4
    fg(ser, CYAN)                           # row 4
    ser.write("  Serveur Minitel v2.0")     # row 4

    # Separator
    utime.sleep_ms(200)
    draw_hline(ser, 5, 1, 40, 0x3F)         # row 5

    # Menu items
    items = [
        ("1", "METEO PARIS",       "Previsions & temperatures"),
        ("2", "TRAFIC RATP",       "Prochains metros en direct"),
    ]

    for i, (num, title, subtitle) in enumerate(items):
        base_row = 7 + i * 4
        move(ser, base_row, 4)
        bg(ser, CYAN)
        fg(ser, BLACK)
        ser.write(" {} ".format(num))
        bg(ser, BLACK)
        fg(ser, WHITE)
        ser.write(" {}".format(title))
        move(ser, base_row + 1, 8)
        fg(ser, CYAN)
        ser.write(subtitle)
        utime.sleep_ms(200)


    # Navigation hints
    utime.sleep_ms(200)
    draw_hline(ser, 21, 1, 40, 0x3F) # row 21

    utime.sleep_ms(200)
    move(ser, 22, 2) # row 22
    fg(ser, GREEN)
    ser.write(BLINK_ON)
    ser.write(">")
    ser.write(BLINK_OFF)
    fg(ser, WHITE)
    ser.write(" Tapez 1 ou 2 puis ENVOI")

    # Footer
    utime.sleep_ms(200)
    fill_row(ser, 24, BLUE, WHITE) # row 24
    move(ser, 24, 1)
    bg(ser, BLUE)
    fg(ser, WHITE)
    ser.write(" (C) 2025 PARIS INFO ")
    fg(ser, WHITE)
    ser.write("   Connexion... ")
    bg(ser, BLACK)
