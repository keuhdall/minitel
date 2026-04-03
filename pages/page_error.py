from utils.minitel_ui import (
    BLACK, WHITE, BLUE,
    NORMAL_SIZE, DOUBLE_SIZE,
    move, fg, bg, fill_row, clear_screen, write_centered,
)


def draw(ser):
    """Draw a WiFi connection error screen (Windows BSOD style)."""
    clear_screen(ser)

    # Fill entire screen with blue background
    for row in range(1, 25):
        fill_row(ser, row, BLUE, WHITE)

    # Sad face :( in double size
    move(ser, 4, 4)
    bg(ser, BLUE)
    fg(ser, WHITE)
    ser.write(DOUBLE_SIZE)
    ser.write(":(")
    ser.write(NORMAL_SIZE)

    # Main error message
    bg(ser, BLUE)
    fg(ser, WHITE)
    move(ser, 9, 4)
    ser.write("Votre Minitel a rencontre")
    move(ser, 10, 4)
    ser.write("un probleme et doit")
    move(ser, 11, 4)
    ser.write("redemarrer.")

    # Details
    move(ser, 14, 4)
    ser.write("Connexion WiFi impossible.")

    # Progress
    move(ser, 17, 4)
    ser.write("0% termine")

    # Restart instruction
    move(ser, 20, 4)
    ser.write("Redemarrez le serveur pour")
    move(ser, 21, 4)
    ser.write("relancer la connexion.")
