# Ensure UART0 is free for Minitel communication.
# MicroPico may configure UART0 as a REPL terminal by default,
# which steals RX bytes when USB is not connected.
import os
try:
    os.dupterm(None)
except:
    pass
