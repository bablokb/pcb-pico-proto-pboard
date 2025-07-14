# -------------------------------------------------------------------------
# Scan available networks: testprogram for the esp32x co-processor.
#
# Author: Bernhard Bablok
# License: MIT
#
# Website: https://github.com/bablokb/pcb-pico-proto-pbard
# -------------------------------------------------------------------------

DEBUG = False
TX_POWER = 15

import busio
import displayio
import time
import wifi
from pboard import pboard

# --- initialize co-processor    ---------------------------------------------

def init_co_processor():
  """ initialize co-processor """

  uart = busio.UART(pboard.ESP_TX, pboard.ESP_RX, baudrate=115200,
                    receiver_buffer_size=2048)
  rc = wifi.init(uart,debug=DEBUG,reset_pin=pboard.ESP_RST)
  if not rc:
    raise RuntimeError("could not setup co-processor")
  wifi.radio.start_station()
  wifi.radio.tx_power = TX_POWER

# --- main program   ---------------------------------------------------------

displayio.release_displays()
display = pboard.eyespi_display()

init_co_processor()

while True:
  print("Available WIFI networks:")
  for n in wifi.radio.start_scanning_networks():
    print(f"  {n.channel:02d}: {n.ssid}")
  wifi.radio.stop_scanning_networks()
  time.sleep(5)
  print("\n\n")
