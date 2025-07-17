import time
import alarm
import displayio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_bme280 import advanced as adafruit_bme280

from pboard import pboard
from pboard import helpers

# --- configuration   --------------------------------------------------------

INTERVAL = 60
DEEP_SLEEP = False
ALTITUDE_AT_LOCATION = 525

# --- class SensorInfo   -----------------------------------------------------

class SensorInfo:
  """ BME280 sensor with display """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._start = time.monotonic()
    # display and UI
    displayio.release_displays()
    self._display = pboard.eyespi_display()
    self._create_ui()

    # create BME280 object
    self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(
      pboard.i2c0(),address=0x76)
    
    # recommended settings: datasheet 3.5.1 weather monitoring
    self._bme280.mode                 = adafruit_bme280.MODE_FORCE
    self._bme280.iir_filter           = adafruit_bme280.IIR_FILTER_DISABLE
    self._bme280.overscan_pressure    = adafruit_bme280.OVERSCAN_X1
    self._bme280.overscan_humidity    = adafruit_bme280.OVERSCAN_X1
    self._bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X1
    self._alt_fac = pow(1.0-ALTITUDE_AT_LOCATION/44330.0, 5.255)

  # --- create UI   ----------------------------------------------------------

  def _create_ui(self):
    """ create UI elements """

    font = bitmap_font.load_font("fonts/DejaVuSans-Bold-24-min.bdf")
    group = displayio.Group()
    self._display.root_group = group

    pos_map = helpers.pos_map(self._display)
    for p in ['NW', 'W', 'SW']:
      pos = pos_map[p]
      # create label at position
      lbl = label.Label(font,color=0xFFFFFF,anchor_point=pos[0])
      lbl.anchored_position = pos[1]
      group.append(lbl)

  # --- read data from sensor   ----------------------------------------------

  def read_data(self):
    """ read data """
    self._data = (self._bme280.temperature,
                  self._bme280.humidity,
                  (self._bme280.pressure/self._alt_fac)
                  )

  # --- show results   -----------------------------------------------------

  def update_ui(self):
    """ update UI with current values """
    print("{0:.1f},{1:0.1f},{2:0.1f},{3:0.1f}".format(
      time.monotonic()-self._start,*self._data))

    for index, (lbl,unit) in enumerate([("Temp", "°C"),
                                        ("Hum", "%rH"),
                                        ("Pres", "hPa")]):
      self._display.root_group[index].text = (
        f"{lbl}: {self._data[index]:0.1f} {unit}")

  # --- loop with light sleep   ----------------------------------------------

  def loop(self):
    """ loop with light sleep """
    while True:
      start = time.monotonic()
      self.read_data()
      self.update_ui()
      time_alarm = alarm.time.TimeAlarm(monotonic_time=start+INTERVAL)
      alarm.light_sleep_until_alarms(time_alarm)

# --- main program   --------------------------------------------------------

sensor_info = SensorInfo()
if DEEP_SLEEP:
  # one shot processing
  sensor_info.read_data()
  sensor_info.update_ui()
  displayio.release_displays()
  time_alarm = alarm.time.TimeAlarm(monotonic_time=start+INTERVAL)
  alarm.exit_and_deep_sleep_until_alarms(time_alarm)
else:
  sensor_info.loop()
