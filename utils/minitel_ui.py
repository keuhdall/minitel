import utime

# Minitel escape sequences
ESC = b'\x1B'
CLR = b'\x0C'
G0 = b'\x0F'  # Alphanumeric mode
G1 = b'\x0E'  # Mosaic/graphics mode

# Colours (foreground = 0x40+c, background = 0x50+c)
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# Text sizes
NORMAL_SIZE = b'\x1B\x4C'
DOUBLE_HEIGHT = b'\x1B\x4D'
DOUBLE_WIDTH = b'\x1B\x4E'
DOUBLE_SIZE = b'\x1B\x4F'

# Minitel key codes
KEY_ENVOI = 0x41      # Send/Select
KEY_RETOUR = 0x42     # Back
KEY_SUITE = 0x48      # Next/Down
KEY_REPETITION = 0x43 # Repeat/Up
KEY_GUIDE = 0x44      # Guide/Home
KEY_SOMMAIRE = 0x46   # Summary/Menu

# Blink
BLINK_ON = b'\x1B\x48'
BLINK_OFF = b'\x1B\x49'


def move(ser, row, col):
    """Move cursor to row, col (1-based)."""
    ser.write(bytes([0x1F, 0x40 + row, 0x40 + col]))


def fg(ser, color):
    """Set the foreground (text) color. Uses ESC + 0x40+color sequence."""
    ser.write(bytes([0x1B, 0x40 + color]))


def bg(ser, color):
    """Set the background color. Uses ESC + 0x50+color sequence."""
    ser.write(bytes([0x1B, 0x50 + color]))


def draw_hline(ser, row, col, length, char=0x23):
    """Draw a horizontal line using mosaic character in G1 mode."""
    move(ser, row, col)
    ser.write(G1)
    bg(ser, BLACK)
    fg(ser, CYAN)
    for _ in range(length):
        ser.write(bytes([char]))
    ser.write(G0)


def draw_box(ser, top, left, width, height, color=CYAN):
    """Draw a rectangular box using G1 mosaic corner and edge characters.
    Renders top-left, top-right, bottom-left, bottom-right corners
    and horizontal/vertical edges at the given position and size."""
    # Top border
    move(ser, top, left)
    ser.write(G1)
    fg(ser, color)
    ser.write(bytes([0x21]))
    for _ in range(width - 2):
        ser.write(bytes([0x24]))
    ser.write(bytes([0x22]))

    # Side borders
    for r in range(top + 1, top + height - 1):
        move(ser, r, left)
        ser.write(G1)
        fg(ser, color)
        ser.write(bytes([0x25]))
        ser.write(G0)
        move(ser, r, left + width - 1)
        ser.write(G1)
        fg(ser, color)
        ser.write(bytes([0x25]))
        ser.write(G0)

    # Bottom border
    move(ser, top + height - 1, left)
    ser.write(G1)
    fg(ser, color)
    ser.write(bytes([0x28]))
    for _ in range(width - 2):
        ser.write(bytes([0x24]))
    ser.write(bytes([0x30]))
    ser.write(G0)


def write_centered(ser, row, text, width=40):
    """Write text centered on the given row."""
    col = (width - len(text)) // 2 + 1
    move(ser, row, col)
    ser.write(text)


def fill_row(ser, row, bg_color=BLACK, fg_color=WHITE):
    """Fill an entire row with a background color.
    fg() is a serial attr (1 cell) + 39 spaces = 40 cells total."""
    move(ser, row, 1)
    bg(ser, bg_color)
    fg(ser, fg_color)
    ser.write(" " * 39)


def clear_screen(ser):
    """Send the clear screen command (0x0C) and reset to white-on-black.
    Includes a 500ms delay to let the Minitel finish clearing.
    Disables the cursor to route keyboard input directly to the host."""
    ser.write(CLR)
    utime.sleep_ms(500)
    ser.write(b'\x14')  # Cursor off — disables local editor
    fg(ser, WHITE)
    bg(ser, BLACK)


def format_time():
    """Return current time as HH:MM string (UTC+2 for Paris/CEST)."""
    t = utime.localtime()
    h = (t[3] + 2) % 24
    return "{:02d}:{:02d}".format(h, t[4])


def read_key(ser, timeout_ms=0):
    """Read a Minitel key press from the UART.
    Function keys are sent as a 2-byte sequence: SEP (0x13) + key code.
    When SEP is detected, waits up to 200ms for the second byte.
    Returns the key code byte, or None if timeout_ms elapses with no input.
    If timeout_ms is 0, blocks until a key is pressed."""
    start = utime.ticks_ms()
    while True:
        if ser.any():
            b = ser.read(1)
            if b and b[0] == 0x13:  # SEP (function key prefix)
                deadline = utime.ticks_ms() + 200
                while utime.ticks_diff(deadline, utime.ticks_ms()) > 0:
                    if ser.any():
                        b2 = ser.read(1)
                        if b2:
                            return b2[0]
                        break
            return b[0] if b else None
        if timeout_ms > 0 and utime.ticks_diff(utime.ticks_ms(), start) > timeout_ms:
            return None
        utime.sleep_ms(50)
