# ----------------------------------------------------------------------------
# Play music using an UART attached DFPlayer Mini.
#
# Needs the DFPlayer library from:
#   https://github.com/bablokb/circuitpython-dfplayer
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-bb
# ----------------------------------------------------------------------------

import board
import digitalio
import time
import busio

from pboard import pboard
from pboard import helpers
from DFPlayer import DFPlayer

# --- main program   ---------------------------------------------------------

helpers.wait_for_console()

uart = pboard.uart0(gp01=True,baudrate=9600)
player = DFPlayer(uart)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

print(f"playing...")
player.play()

while True:
  time.sleep(0.2)
  led.value = False
  time.sleep(0.2)
  led.value = True
