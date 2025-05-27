Pins
====


Pins on Raspberry Pi Pico
-------------------------



|                     | Pin  | Pin  |                         |
|---------------------|------|------|-------------------------|
| TX0                 | GP0  | VBUS |
| RX0                 | GP1  | VSYS |
|                     | GND  | GND  |
| I2C1-SDA (RTC, I2C) | GP2  | EN   |
| I2C1-SCL (RTC, I2C) | GP3  | 3V3  |
| RTC-INT             | GP4  | VREF |
| COUT/SIG/BTN3       | GP5  | GP28 | TPL5110 DONE
|                     | GND  | GND  |
| BTN1                | GP6  | GP27 | ADC
| BTN2                | GP7  | GP26 | Display BL/Busy (EYESPI)
| MISO1/I2S_DATA/BSY1 | GP8  | RUN  | RUN
| DC1/I2S_MUTE        | GP9  | GP22 | Display DC
|                     | GND  | GND  |
| SCK1/I2S_BLK        | GP10 | GP21 | Display Reset (EYESPI)
| MOSI1/I2S_WSEL      | GP11 | GP20 | Display CS (EYESPI)
| TX0 (ESP-01S-RX,    | GP12 | GP19 | MOSI0 (EYESPI, SD-Card)
|      EYESPI-SDA0)   |      |      |
| RX0 (ESP-01S-TX,    | GP13 | GP18 | SCLK0 (EYESPI, SD-Card)
|      EYESPI-SCL0)   |      |      |
|                     | GND  | GND  |
| RST-ESP01 (7)/RST1  | GP14 | GP17 | SD CS (EYESPI)
|      EYESPI-TS_CS)  |      |      |
| IO2-ESP01 (2)/CS1   | GP15 | GP16 | MISO0 (EYESPI, SD-Card)
|      EYESPI-INT)    |      |      |


Pins on EYESPI
--------------

Use the onboard jumper-pad to select between
backlight and busy. TFT-displays use the backlight-pin while
e-paper displays use the busy-pin.


| Pin | Func    | Mapped to
|-----|---------|-------------------------|
|   1 | GPIO2   | n.c.
|   2 | GPIO1   | n.c.
|   3 | BUSY    | GP26 (alternative)
|   4 | INT     | GP15
|   5 | SDA     | GP12
|   6 | SCL     | GP13
|   7 | TS_CS   | GP14
|   8 | MEM_CS  | n.c.
|   9 | SD_CS   | GP17
|  10 | DISP_CS | GP20
|  11 | RESET   | GP21
|  12 | DC      | GP22
|  13 | MISO    | GP16
|  14 | MOSI    | GP19
|  15 | SCK     | GP18
|  16 | GND     | GND
|  17 | BLITE   | GP26 (default)
|  18 | VCC     | 3V3

