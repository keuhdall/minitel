import utime
import apis.idfm as idfm
from utils.minitel_ui import (
    G0, G1,
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
    NORMAL_SIZE, DOUBLE_HEIGHT,
    BLINK_ON, BLINK_OFF,
    move, fg, bg, draw_hline, draw_box, fill_row, clear_screen, format_time,
)


def draw(ser):
    """Draw the full RATP transit page."""
    clear_screen(ser)

    # Header
    # Header - title on row 2 so double-height top half extends into row 1
    fill_row(ser, 1, MAGENTA, WHITE)
    fill_row(ser, 2, MAGENTA, WHITE)
    move(ser, 2, 1)
    bg(ser, MAGENTA)
    fg(ser, WHITE)
    ser.write(DOUBLE_HEIGHT)
    ser.write(" TRAFIC RATP")
    ser.write(NORMAL_SIZE)

    fill_row(ser, 3, MAGENTA, YELLOW)
    move(ser, 3, 1)
    bg(ser, MAGENTA)
    fg(ser, YELLOW)
    ser.write("  Horaires temps reel - {}".format(format_time()))
    bg(ser, BLACK)

    # Separator
    utime.sleep_ms(200)
    draw_hline(ser, 4, 1, 40, 0x3F)

    # Section title
    move(ser, 5, 1)
    bg(ser, BLUE)
    fg(ser, WHITE)
    ser.write(" PROCHAINS DEPARTS                     ")
    bg(ser, BLACK)

    row = 7
    stations = idfm.get_stations()
    for i, station in enumerate(stations):
        delay = idfm.get_next_train(station["id"])
        _draw_station_row(ser, row, station, delay)
        row += 1

        # Separator between entries
        if i < len(stations) - 1:
            move(ser, row, 3)
            fg(ser, CYAN)
            ser.write(G1)
            for _ in range(34):
                ser.write(bytes([0x24]))
            ser.write(G0)
            row += 1

    # Info box
    utime.sleep_ms(200)
    info_row = row + 2
    draw_box(ser, info_row, 2, 38, 3, CYAN)
    move(ser, info_row + 1, 4)
    fg(ser, CYAN)
    ser.write("Donnees IDFM - Rafraichi/2min")

    # Navigation
    utime.sleep_ms(200)
    draw_hline(ser, 22, 1, 40, 0x3F)
    utime.sleep_ms(200)
    move(ser, 23, 2)
    fg(ser, GREEN)
    ser.write("SOMMAIRE: Menu  SUITE: Rafraichir")

    # Footer — 2 fg serial attrs + 38 text chars = 40 cells (no row-24 scroll)
    utime.sleep_ms(200)
    fill_row(ser, 24, MAGENTA, WHITE)
    move(ser, 24, 1)
    bg(ser, MAGENTA)
    fg(ser, WHITE)                                     # col 1 (serial attr)
    ser.write(" 3615 RATP-DIRECT  ")                   # cols 2-20 (19 chars)
    fg(ser, YELLOW)                                    # col 21 (serial attr)
    ser.write("              {}".format(format_time())) # cols 22-40 (19 chars)
    bg(ser, BLACK)


def _draw_station_row(ser, row, station, delay):
    """Draw a single station departure row."""
    # Line badge with color coding
    move(ser, row, 2)
    fg(ser, WHITE)
    if station["line"] == "2":
        bg(ser, BLUE)
    elif station["line"] == "12":
        bg(ser, GREEN)
    else:
        bg(ser, CYAN)
    ser.write(" M{} ".format(station["line"]))
    bg(ser, BLACK)

    # Direction
    move(ser, row, 8)
    fg(ser, YELLOW)
    direction = station["direction"]
    if len(direction) > 18:
        direction = direction[:18]
    ser.write(direction)

    # Time display
    if delay is not None:
        minutes = delay // 60
        move(ser, row, 30)
        if minutes <= 1:
            fg(ser, RED)
            ser.write(BLINK_ON)
            ser.write("{:>3} min".format(minutes))
            ser.write(BLINK_OFF)
        elif minutes <= 3:
            fg(ser, YELLOW)
            ser.write("{:>3} min".format(minutes))
        else:
            fg(ser, WHITE)
            ser.write("{:>3} min".format(minutes))
    else:
        move(ser, row, 30)
        fg(ser, RED)
        ser.write("  ----")
