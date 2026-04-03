# Minitel

A retro Minitel terminal server that brings modern data to vintage 1980s French hardware. Built with MicroPython on a Raspberry Pi Pico, it displays real-time Paris weather and metro departures using the authentic Minitel videotex protocol.

## Demo
[![](https://markdown-videos-api.jorgenkh.no/youtube/aUsJFpJNq2Y)](https://youtu.be/aUsJFpJNq2Y)

## Features

- **Weather Forecasts (METEO PARIS)** — Current conditions for Paris via OpenWeatherMap: temperature, humidity, pressure, and weather icons rendered in Minitel mosaic graphics. Color-coded by temperature.
- **Metro Departures (TRAFIC RATP)** — Real-time Paris metro arrival times via the Île-de-France Mobilités API. Line-colored badges, station names, and countdown timers with urgency color coding.
- **Authentic Minitel UI** — Full videotex escape sequences, 8-color palette, double-height/double-width text, mosaic (G1) graphics mode, and classic navigation with ENVOI, SOMMAIRE, SUITE, and RETOUR keys.
- **Auto-refresh** — Both pages update automatically every 2 minutes.
- **Graceful error handling** — Falls back to a dedicated error screen on WiFi failure.

## Hardware

- Raspberry Pi Pico (RP2040)
- Minitel terminal connected via UART
- WiFi network

## Setup

1. Flash MicroPython onto the Raspberry Pi Pico.

2. Set your WiFi credentials in `main.py`:
   ```python
   SSID = "your_network"
   PASSWORD = "your_password"
   ```

3. Set your API keys:
   - `apis/weather.py` — `API_KEY` for [OpenWeatherMap](https://openweathermap.org/api)
   - `apis/idfm.py` — `API_KEY` for [IDFM (Île-de-France Mobilités)](https://prim.iledefrance-mobilites.fr/)
   - Pick the stations you want to monitor (currently set to Pigalle)

4. Upload all files to the Pico's filesystem (e.g. using [MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) for VS Code).

5. Power up — `main.py` runs automatically.

## Usage

| Key        | Action                     |
|------------|----------------------------|
| `1` / `2`  | Select menu option         |
| `ENVOI`    | Confirm selection          |
| `SOMMAIRE` | Return to main menu        |
| `RETOUR`   | Return to main menu        |
| `SUITE`    | Refresh current page       |

## Technical Details

- **State machine architecture** with 4 states: Menu, Weather, RATP, and Error
- **UART communication** at 4800 baud (after initial 1200 baud handshake), 7-bit with even parity
- **NTP time sync** adjusted to Paris timezone (UTC+2)
- All rendering uses Minitel-native videotex escape codes — no framebuffer, no modern display stack
