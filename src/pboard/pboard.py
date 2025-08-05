# ----------------------------------------------------------------------------
# Proto-Board pin definitions and helper-methods.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-pboard
# ----------------------------------------------------------------------------

import board
import busio

# I2C
SDA0 = board.GP0  # also TX0
SCL0 = board.GP1  # also RX0
SDA1 = board.GP2
SCL1 = board.GP3

# RTC
RTC_INT  = board.GP4
RTC_COUT = board.GP5

# PWM, buttons, sensor-button
SIG  = board.GP5
BTN0 = board.GP6
BTN1 = board.GP7
BTN2 = board.GP5
BTN  = [BTN0, BTN1, BTN2]

# TPL5110, ADC
TPL_DONE = board.GP28
ADC      = board.GP27

# EYESPI
EYESPI_SCK0  = board.GP18
EYESPI_MOSI0 = board.GP19
EYESPI_MISO0 = board.GP16
EYESPI_DC    = board.GP22
EYESPI_RST   = board.GP21

EYESPI_BL   = board.GP26
EYESPI_Busy = board.GP26
EYESPI_INT  = board.GP15

EYESPI_DSP_CS = board.GP20
EYESPI_TS_CS  = board.GP14
EYESPI_SD_CS  = board.GP17

EYESPI_SDA0 = board.GP12
EYESPI_SCL0 = board.GP13

# I2S
I2S_WSEL = board.GP11
I2S_BLK = board.GP10
I2S_DATA = board.GP8
I2S_MUTE = board.GP9

# SPI1
SCK1  = board.GP10
MOSI1 = board.GP11
MISO1 = board.GP8
CS1   = board.GP15
DC1   = board.GP9
RST1  = board.GP14
BUSY1 = board.GP8

# UART
TX0 = board.GP12    # also on board.GP0
RX0 = board.GP13    # also on board.GP1

# ESP
ESP_TX  = board.GP12 # RX-pin on ESP01-S
ESP_RX  = board.GP13 # TX-pin on ESP01-S
ESP_RST = board.GP14 # pin 7 on ESP01-S
ESP_IO2 = board.GP15 # pin 2 on ESP-01

# SD-card
SD_MOSI = board.GP19
SD_SCK  = board.GP18
SD_MISO = board.GP16
SD_CS   = board.GP17

# --- create OLED-display   --------------------------------------------------

_oled = None
def oled_display(width=128,height=64,address=0x3c,**kwargs):
  """ return OLED-display object (create if necessary) """
  global _oled
  if not _oled:
    from i2cdisplaybus import I2CDisplayBus
    from adafruit_displayio_ssd1306 import SSD1306
    display_bus = I2CDisplayBus(i2c1(),device_address=address)
    _oled = SSD1306(display_bus,width=width,height=height,**kwargs)
  return _oled

# --- create EYESPI-display   ------------------------------------------------

_spi_display = None
def eyespi_display(driver=None,**kwargs):
  """ return SPI-display,(create if necessary) """
  global _spi_display
  if not _spi_display:
    import fourwire
    bus = fourwire.FourWire(spi0(),
                            command=EYESPI_DC,
                            chip_select=EYESPI_DSP_CS,
                            reset=EYESPI_RST)
    if driver:
      _spi_display = driver(bus,**kwargs)
    else:
      from adafruit_st7789 import ST7789
      _spi_display = ST7789(bus, width=320, height=240, rotation=270,
                            backlight_pin=EYESPI_BL,
                            brightness=0.6)
  return _spi_display

# --- create I2C0-bus   ------------------------------------------------------

_i2c0 = None
def i2c0():
  """ return i2c0 (create if necessary) """
  global _i2c0
  if not _i2c0:
    _i2c0 = busio.I2C(SCL0,SDA0)
  return _i2c0

# --- create I2C1-bus   ------------------------------------------------------

_i2c1 = None
def i2c1():
  """ return i2c1 (create if necessary) """
  global _i2c1
  if not _i2c1:
    _i2c1 = busio.I2C(SCL1,SDA1)
  return _i2c1

# --- create SPI0-bus   ------------------------------------------------------

_spi0 = None
def spi0(miso=SD_MISO):
  """ return spi0 (create if necessary) """
  global _spi0
  if not _spi0:
    _spi0 = busio.SPI(SD_SCK,SD_MOSI,miso)
  return _spi0

# --- create SPI1-bus   ------------------------------------------------------

_spi1 = None
def spi1(miso=MISO1):
  """ return spi1 (create if necessary) """
  global _spi1
  if not _spi1:
    _spi1 = busio.SPI(SCK1,MOSI1,miso)
  return _spi1

# --- create UART0   ---------------------------------------------------------

_uart0 = None
def uart0(gp01=False,baudrate=115200):
  """ return uart0 (create if necessary) """
  global _uart0
  if not _uart0:
    if gp01:
      _uart0 = busio.UART(SDA0, SCL0, baudrate=baudrate)
    else:
      _uart0 = busio.UART(TX0, RX0, baudrate=baudrate)
  return _uart0

# --- create RTC (with PCF8563)   --------------------------------------------

_rtc = None
def rtc():
  """ return rtc-object (create if necessary) """
  global _rtc
  if not _rtc:
    from adafruit_pcf8563.pcf8563 import PCF8563
    _rtc = PCF8563(i2c1())
  return _rtc

# --- create buzzer   --------------------------------------------------------

_buzzer = None
def buzzer(simple=False):
  """ return AsyncBuzzer (create if necessary) """
  global _buzzer
  if not _buzzer:
    if simple:
      import pwmio
      _buzzer = pwmio.PWMOut(SIG,variable_frequency=True)
    else:
      from buzzer_music.async_buzzer import AsyncBuzzer
      _buzzer = AsyncBuzzer(SIG)
  return _buzzer

# --- create button   --------------------------------------------------------

_btn = [None,None,None]
def button(index, active_low=True):
  """ create button (index is left to right) """
  global _btn
  if not _btn[index]:
    from digitalio import DigitalInOut, Direction, Pull
    _btn[index] = DigitalInOut(BTN[index])
    _btn[index].pull = Pull.UP if active_low else Pull.DOWN
  return _btn[index]

# --- signal done-pin   ------------------------------------------------------

_done = None
def tpl_setup():
  """ setup DONE-pin for TPL5110 """
  global _done
  if not _done:
    # create
    from digitalio import DigitalInOut, Direction, Pull
    _done           = DigitalInOut(TPL_DONE)
    _done.pull      = Pull.DOWN
    _done.direction = Direction.OUTPUT
    _done.value     = False

def tpl_poweroff():
  """ signal power-off """
  global _done
  if not _done:
    tpl_setup()
  import time
  _done.value = True
  time.sleep(0.01)
  _done.value = False

# --- create I2S audiobus and mute-pin   -------------------------------------

_i2s = None
_mute = None
def i2s():
  """ create I2S bus """
  import audiobusio
  import digitalio
  global _i2s, _mute
  if not _i2s:
    # create bus
    _i2s = audiobusio.I2SOut(I2S_BLK, I2S_WSEL, I2S_DATA) #  BLCK, WSEL, DATA
    # create mute-pin and start unmuted
    _mute = digitalio.DigitalInOut(I2S_MUTE)
    _mute.switch_to_output(value=True)
  return (_i2s,_mute)

# --- mount SD-card   --------------------------------------------------------

def mount_sd():
  """mount SD-sdcard"""
  import sdcardio
  import storage
  sdcard = sdcardio.SDCard(spi0(),SD_CS,1_000_000)
  vfs    = storage.VfsFat(sdcard)
  storage.mount(vfs, "/sd")

# --- read ADC-value   -------------------------------------------------------

_adc = None
def adc_setup():
  """ create ADC """
  global _adc
  if not _adc:
    from analogio import AnalogIn
    _adc = AnalogIn(ADC)

def adc_read():
  """ read ADC-value and convert """
    
  if not _adc:
    adc_setup()
    # voltage divider signal -> 10K ->      -> 15K - GND
    #                               -> _adc
    return _adc.value * 1.6666667 * 3.3 / 65535

