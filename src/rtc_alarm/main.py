# ----------------------------------------------------------------------------
# Deep-Sleep with RTC wake up.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-bb
# ----------------------------------------------------------------------------

import alarm
import atexit
import board
import busio
import digitalio
import rtc
import microcontroller
import socketpool
import time
import wifi

import displayio
import terminalio
import adafruit_requests
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from pboard import pboard
from pboard import helpers
from secrets import secrets

USE_OLED = True
SLEEP_TIME = 50
WORK_TIME = 10
DEBUG = False
TX_POWER = 15

# --- initialize co-processor    ---------------------------------------------

def init_coprocessor():
  """ initialize co-processor """

  uart = busio.UART(pboard.ESP_TX, pboard.ESP_RX, baudrate=115200,
                    receiver_buffer_size=2048)
  rc = wifi.init(uart,debug=DEBUG,reset_pin=pboard.ESP_RST)
  if not rc:
    raise RuntimeError("could not setup co-processor")
  wifi.radio.start_station()
  wifi.radio.tx_power = TX_POWER

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

# --- connect and update RTC   -----------------------------------------------

def update_rtc(ext_rtc):
  """ update RTC """
  helpers.connect()
  ts = get_remote_time()
  ext_rtc.datetime = ts
  int_rtc = rtc.RTC()
  int_rtc.datetime = ts

# --- atexit processing   ----------------------------------------------------

def at_exit(i2c):
  """ release i2c """
  print(f"releasing {i2c}")
  i2c.deinit()

# --- main program   ---------------------------------------------------------

#helpers.wait_for_console()

# setup board LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False

# check reset reason
rr_reason = (f"{microcontroller.cpu.reset_reason}").split(".")[-1]
print(f"reset reason: {rr_reason}")

# fetch time and update RTC
ext_rtc = pboard.rtc()
if rr_reason == "POWER_ON":
  print("updating RTC")
  init_coprocessor()
  update_rtc(ext_rtc)
else:
  # assume time is valid
  print("clearing alarm")
  ext_rtc.alarm_status = False
  ext_rtc.alarm_interrupt = False
  ts = ext_rtc.datetime
  rtc.RTC().datetime = ts

# release I2C1 at exit (allocated by rtc)
atexit.register(at_exit,pboard.i2c1())
atexit.register(displayio.release_displays)

# create display
displayio.release_displays()
if USE_OLED:
  display = pboard.oled_display(rotation=180)
else:
  display = pboard.eyespi_display()        # use default display

# create labels
# upper boarder: reset-reason
pos = helpers.pos_map(display)['N']
txt_reason = label.Label(terminalio.FONT,text=rr_reason,color=0xFFFFFF,
                       anchor_point=pos[0])
txt_reason.anchored_position = pos[1]

# center: time
pos = helpers.pos_map(display)['C']
font = bitmap_font.load_font("fonts/DejaVuSans-Bold-24-min.bdf")
txt_time = label.Label(font,text='00:00:00',color=0xFFFFFF,
                       anchor_point=pos[0])
txt_time.anchored_position = pos[1]

# lower boarder: state
pos = helpers.pos_map(display)['S']
txt_state = label.Label(terminalio.FONT,text='active',color=0xFFFFFF,
                        anchor_point=pos[0])
txt_state.anchored_position = pos[1]

# create and set root-group
group = displayio.Group()
group.append(txt_reason)
group.append(txt_time)
group.append(txt_state)
display.root_group = group

# do some work
for _ in range(WORK_TIME):
  now = time.localtime()
  txt_time.text = f"{now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"
  for __ in range(4):
    time.sleep(0.125)
    led.value = not led.value
    time.sleep(0.125)
    led.value = not led.value

# switch display
txt_state.text = "sleep"
time.sleep(1)

# set wake up time and create pin-alarm
alarm_time = time.mktime(now) + SLEEP_TIME
print(f"deep-sleep for {SLEEP_TIME} seconds")
pin_alarm = alarm.pin.PinAlarm(pboard.RTC_INT,
                               value=False,edge=True,pull=True)
ext_rtc.alarm  = (time.localtime(alarm_time),"daily")
ext_rtc.alarm_interrupt = True

alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

time.sleep(1)
print("we should not be here!")
