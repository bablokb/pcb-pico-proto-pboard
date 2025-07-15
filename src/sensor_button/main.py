# ----------------------------------------------------------------------------
# Test sensor-button (TTP223B) operation.
#
# The sensor has three pins (3V3,GND,SIG) and is pulled high on touch.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-bb
# ----------------------------------------------------------------------------

import board
import time
import digitalio
from pboard import pboard

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

button = pboard.button(2,active_low=False)  # SIG pin shares pin with BTN2

print("touch the button to blink the on-board LED...")
while True:
  if button.value:
    print("touch detected!")
    for _ in range(3):
      led.value = 1
      time.sleep(0.1)
      led.value = 0
      time.sleep(0.1)
