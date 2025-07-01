# ----------------------------------------------------------------------------
# Update RTC-time and show time on OLED/EYESPI.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-bb
# ----------------------------------------------------------------------------

import atexit
import rtc
import socketpool
import time
import wifi

import displayio
import adafruit_requests
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from pboard import pboard
from pboard import helpers
from secrets import secrets

# --- query local time from time-server   ---------------------------------

def get_remote_time():
  """ query time from time-server """

  pool = socketpool.SocketPool(wifi.radio)
  requests = adafruit_requests.Session(pool)

  response = requests.get(secrets['time_api_url']).json()

  if 'struct_time' in response:
    return time.struct_time(tuple(response['struct_time']))

  current_time = response["datetime"]
  the_date, the_time = current_time.split("T")
  year, month, mday = [int(x) for x in the_date.split("-")]
  the_time = the_time.split(".")[0]
  hours, minutes, seconds = [int(x) for x in the_time.split(":")]

  year_day = int(response["day_of_year"])
  week_day = int(response["day_of_week"])
  week_day = 6 if week_day == 0 else week_day-1
  is_dst   = int(response["dst"])

  return time.struct_time(
    (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst))

# --- atexit processing   ----------------------------------------------------

def at_exit(i2c):
  """ release i2c """
  print(f"releasing {i2c}")
  i2c.deinit()

# --- main program   ---------------------------------------------------------

# check BTN0 at startup
btn = pboard.button(0)
use_oled = btn.value

helpers.wait_for_console()
helpers.connect()

# fetch time and update RTC
ts = get_remote_time()
ext_rtc = pboard.rtc()
ext_rtc.datetime = ts
int_rtc = rtc.RTC()
int_rtc.datetime = ts

# release I2C1 at exit (allocated by rtc)
atexit.register(at_exit,pboard.i2c1())

# create display
displayio.release_displays()
if use_oled:
  print("BTN0 not pressed, using OLED")
  display = pboard.oled_display(rotation=180)
else:
  print("BTN0 pressed, using EYESPI")
  from adafruit_st7789 import ST7789
  display = pboard.eyespi_display(ST7789,
                           width=320, height=240, rotation=270,
                           backlight_pin=pboard.EYESPI_BL,
                           brightness=0.6)

# fetch center-position
pos = helpers.pos_map(display)['C']

# create label at center for time
font = bitmap_font.load_font("fonts/DejaVuSans-Bold-24-min.bdf")
txt_time = label.Label(font,text='00:00:00',color=0xFFFFFF,
                       anchor_point=pos[0])
txt_time.anchored_position = pos[1]

# create and set root-group
group = displayio.Group()
group.append(txt_time)
display.root_group = group

# loop and update time using autorefresh 
while True:
  t = time.localtime()
  txt_time.text = f"{t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"
  time.sleep(1)
