import utime
import apis.weather as weather
import utils.weather_images as weather_images
from utils.minitel_ui import (
    G0, G1,
    BLACK, RED, GREEN, YELLOW, BLUE, CYAN, WHITE,
    NORMAL_SIZE, DOUBLE_SIZE,
    move, fg, bg, draw_hline, fill_row, clear_screen, format_time,
)


def draw(ser):
    """Draw the full weather page."""
    clear_screen(ser)

    # Header - title on row 2 so double-size top half extends into row 1
    fill_row(ser, 1, CYAN, BLACK)
    fill_row(ser, 2, CYAN, BLACK)
    move(ser, 2, 1)
    bg(ser, CYAN)
    fg(ser, BLACK)
    ser.write(DOUBLE_SIZE)
    ser.write(" METEO PARIS")
    ser.write(NORMAL_SIZE)

    fill_row(ser, 3, CYAN, WHITE)
    move(ser, 3, 1)
    bg(ser, CYAN)
    fg(ser, WHITE)
    ser.write("  Mise a jour: {}".format(format_time()))
    bg(ser, BLACK)

    # Separator
    utime.sleep_ms(200)
    draw_hline(ser, 4, 1, 40, 0x3F)

    # Fetch weather data
    weather_data = weather.get_weather()

    if weather_data:
        _draw_weather_data(ser, weather_data)
    else:
        move(ser, 8, 5)
        fg(ser, RED)
        ser.write("Donnees meteo indisponibles")
        move(ser, 10, 5)
        fg(ser, WHITE)
        ser.write("Verifiez la connexion...")

    # Navigation
    utime.sleep_ms(200)
    draw_hline(ser, 22, 1, 40, 0x3F)
    utime.sleep_ms(200)
    move(ser, 23, 2)
    fg(ser, GREEN)
    ser.write("SOMMAIRE: Menu  SUITE: Rafraichir")

    # Footer — 2 fg serial attrs + 38 text chars = 40 cells (no row-24 scroll)
    utime.sleep_ms(200)
    fill_row(ser, 24, CYAN, BLACK)
    move(ser, 24, 1)
    bg(ser, CYAN)
    fg(ser, BLACK)                                     # col 1 (serial attr)
    ser.write(" 3615 METEO-PARIS  ")                   # cols 2-20 (19 chars)
    fg(ser, WHITE)                                     # col 21 (serial attr)
    ser.write("              {}".format(format_time())) # cols 22-40 (19 chars)


def _strip_accents(text):
    """Replace accented characters with ASCII equivalents for Minitel."""
    _map = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'À': 'A', 'Â': 'A',
        'Ù': 'U', 'Û': 'U',
        'Ô': 'O', 'Î': 'I',
        'Ç': 'C',
    }
    for accented, plain in _map.items():
        text = text.replace(accented, plain)
    return text


def _draw_weather_data(ser, data):
    """Draw weather icon, temperature, and details."""
    # Weather icon (left side, rows ~7-17)
    img = weather_images.get_image_for_weather_id(data["id"])
    if img:
        ser.write(img)
    ser.write(G0)  # Reset to text mode after image

    # Temperature - big display (right of image, row 7 so double-size
    # extends to row 6 without overlapping the separator at row 4)
    move(ser, 7, 18)
    fg(ser, WHITE)
    bg(ser, BLACK)
    ser.write(DOUBLE_SIZE)
    ser.write("{:.0f}*C".format(data["temp"]))
    ser.write(NORMAL_SIZE)

    # Description
    move(ser, 9, 18)
    fg(ser, YELLOW)
    desc = _strip_accents(data["desc"])
    if len(desc) > 22:
        desc = desc[:22]
    ser.write(desc[0].upper() + desc[1:] if len(desc) > 1 else desc.upper())

    # Details (right of image to avoid overlap)
    move(ser, 11, 18)
    fg(ser, CYAN)
    ser.write("Humidite: ")
    fg(ser, WHITE)
    ser.write("{}%".format(data["hum"]))

    move(ser, 13, 18)
    fg(ser, CYAN)
    ser.write("Pression: ")
    fg(ser, WHITE)
    ser.write("{} hPa".format(data["pres"]))

    # Temperature with color coding
    move(ser, 15, 18)
    fg(ser, CYAN)
    ser.write("Temp: ")
    temp = data["temp"]
    if temp <= 0:
        fg(ser, BLUE)
    elif temp <= 10:
        fg(ser, CYAN)
    elif temp <= 20:
        fg(ser, GREEN)
    elif temp <= 30:
        fg(ser, YELLOW)
    else:
        fg(ser, RED)
    ser.write("{:.1f}*C".format(temp))
