from utils.minitel_ui import (
    BLACK, RED, WHITE, BLUE, CYAN,
    NORMAL_SIZE, DOUBLE_HEIGHT,
    move, fg, bg, draw_hline, fill_row, clear_screen, write_centered,
)


def draw(ser):
    """Draw a WiFi connection error screen."""
    clear_screen(ser)

    # Title
    fill_row(ser, 1, BLUE, WHITE)
    fill_row(ser, 2, BLUE, WHITE)
    move(ser, 2, 1)
    bg(ser, BLUE)
    fg(ser, WHITE)
    ser.write(DOUBLE_HEIGHT)
    ser.write("  3615 PARIS INFO")
    ser.write(NORMAL_SIZE)

    fill_row(ser, 3, BLUE, WHITE)

    # Separator
    draw_hline(ser, 5, 1, 40, 0x3F)

    # Error message
    move(ser, 9, 1)
    fg(ser, RED)
    write_centered(ser, 9, "ERREUR DE CONNEXION")

    move(ser, 12, 1)
    fg(ser, WHITE)
    write_centered(ser, 12, "Impossible de se connecter")
    write_centered(ser, 13, "au reseau WiFi.")

    write_centered(ser, 16, "Verifiez votre connexion")
    write_centered(ser, 17, "et redemarrez le serveur.")

    # Separator
    draw_hline(ser, 21, 1, 40, 0x3F)

    # Footer
    fill_row(ser, 24, BLUE, WHITE)
    move(ser, 24, 1)
    bg(ser, BLUE)
    fg(ser, WHITE)
    ser.write(" (C) 2025 PARIS INFO ")
    bg(ser, BLACK)
