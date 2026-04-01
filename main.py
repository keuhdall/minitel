from machine import UART, Pin
import utils.wifi as wifi
import ntptime
import utime
from utils.minitel_ui import (
    KEY_ENVOI, KEY_RETOUR, KEY_SUITE, KEY_SOMMAIRE,
    read_key,
)
import pages.page_menu as page_menu
import pages.page_weather as page_weather
import pages.page_ratp as page_ratp
import pages.page_error as page_error


SSID = ""
PASSWORD = ""

STATE_MENU = 0
STATE_WEATHER = 1
STATE_RATP = 2
STATE_ERROR = 3

AUTO_REFRESH_MS = 120000


# Switch Minitel from default 1200 baud to 4800 baud
ser = UART(0, 1200, bits=7, parity=2, stop=1)
ser.write(b'\x1B\x3A\x6B\x76')
utime.sleep_ms(300)
# Fully release UART0 and reclaim RX pin before reinit at 4800
ser.deinit()
Pin(1, Pin.IN, Pin.PULL_UP)
ser = UART(0, 4800, bits=7, parity=2, stop=1)

if wifi.connect(SSID, PASSWORD):
    ntptime.settime()
    state = STATE_MENU
else:
    state = STATE_ERROR
menu_choice = None
needs_redraw = True
last_refresh = 0


def flush_uart(ser):
    """Discard any stray bytes left in the UART receive buffer."""
    while ser.any():
        ser.read(1)


while True:
    if state == STATE_MENU:
        if needs_redraw:
            page_menu.draw(ser)
            flush_uart(ser)
            needs_redraw = False

        key = read_key(ser, timeout_ms=0)
        if key == ord('1'):
            menu_choice = 1
        elif key == ord('2'):
            menu_choice = 2
        elif key == KEY_ENVOI and menu_choice is not None:
            if menu_choice == 1:
                state = STATE_WEATHER
            elif menu_choice == 2:
                state = STATE_RATP
            menu_choice = None
            needs_redraw = True

    elif state == STATE_WEATHER:
        if needs_redraw:
            page_weather.draw(ser)
            flush_uart(ser)
            needs_redraw = False
            last_refresh = utime.ticks_ms()

        key = read_key(ser, timeout_ms=500)
        if key == KEY_SOMMAIRE or key == KEY_RETOUR:
            state = STATE_MENU
            needs_redraw = True
        elif key == KEY_SUITE:
            needs_redraw = True
        elif utime.ticks_diff(utime.ticks_ms(), last_refresh) > AUTO_REFRESH_MS:
            needs_redraw = True

    elif state == STATE_RATP:
        if needs_redraw:
            page_ratp.draw(ser)
            flush_uart(ser)
            needs_redraw = False
            last_refresh = utime.ticks_ms()

        key = read_key(ser, timeout_ms=500)
        if key == KEY_SOMMAIRE or key == KEY_RETOUR:
            state = STATE_MENU
            needs_redraw = True
        elif key == KEY_SUITE:
            needs_redraw = True
        elif utime.ticks_diff(utime.ticks_ms(), last_refresh) > AUTO_REFRESH_MS:
            needs_redraw = True

    elif state == STATE_ERROR:
        if needs_redraw:
            page_error.draw(ser)
            flush_uart(ser)
            needs_redraw = False

        read_key(ser, timeout_ms=0)
