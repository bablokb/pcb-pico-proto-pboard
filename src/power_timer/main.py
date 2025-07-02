# ----------------------------------------------------------------------------
# Testprogram for TPL5110 power-timer.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-bb
# ----------------------------------------------------------------------------

import board
import displayio
import time
from digitalio import DigitalInOut, Direction, Pull

from pboard import pboard

# --- initialization   -------------------------------------------------------

led           = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
pboard.tpl_setup()

# create display for console output
displayio.release_displays()
display = pboard.eyespi_display()        # use default display

# --- simulate work   --------------------------------------------------------

WORK_TIME = 10
LED_TIME = 1
def work():
  print(f"working for {WORK_TIME}s...")
  start = time.monotonic()
  end = start + WORK_TIME-2*LED_TIME
  while time.monotonic() < end:
    led.value = 1
    time.sleep(LED_TIME)
    led.value = 0
    time.sleep(LED_TIME)

# --- main loop   ------------------------------------------------------------

print("starting to work")
work()
print("finished work")

print("setting DONE pin to turn power off")
pboard.tpl_poweroff()

# this code should not run
print("entering endless loop")
while True:
  time.sleep(1)
