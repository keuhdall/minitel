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
ser = UART(0, 4800, bits=7, parity=2, stop=1)

# ---- DIAGNOSTIC: raw GPIO test on RX pin (GP1) ----
# Temporarily release UART so we can read GP1 as plain GPIO.
ser.deinit()
rx_pin = Pin(1, Pin.IN, Pin.PULL_UP)
tx_ser = UART(0, 4800, bits=7, parity=2, stop=1, tx=Pin(0))

tx_ser.write(b'\x0C')  # clear screen
utime.sleep_ms(500)
tx_ser.write(b'\x1F\x43\x41')  # move row 3, col 1
tx_ser.write(b'GPIO TEST - press keys on Minitel')
tx_ser.write(b'\x1F\x45\x41')  # move row 5, col 1
tx_ser.write(b'Counting signal changes on GP1...')

last_val = rx_pin.value()
transitions = 0
start = utime.ticks_ms()
while utime.ticks_diff(utime.ticks_ms(), start) < 10000:  # 10 seconds
    val = rx_pin.value()
    if val != last_val:
        transitions += 1
        last_val = val
    # Update display every 500ms
    elapsed = utime.ticks_diff(utime.ticks_ms(), start)
    if elapsed % 500 < 20:
        tx_ser.write(b'\x1F\x47\x41')  # move row 7, col 1
        tx_ser.write('Transitions: {}  Time: {}s  '.format(
            transitions, elapsed // 1000))

tx_ser.write(b'\x1F\x49\x41')  # move row 9, col 1
if transitions > 0:
    tx_ser.write('PASS - GP1 receives signal!')
else:
    tx_ser.write('FAIL - GP1 sees no signal.')

tx_ser.write(b'\x1F\x4B\x41')  # move row 11, col 1
tx_ser.write(b'Continuing to normal boot in 5s...')
utime.sleep_ms(5000)

# Restore normal UART
tx_ser.deinit()
ser = UART(0, 4800, bits=7, parity=2, stop=1)
# ---- END DIAGNOSTIC ----

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
