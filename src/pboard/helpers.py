# ----------------------------------------------------------------------------
# Generic helper methods.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-pboard
# ----------------------------------------------------------------------------

# --- wait for connected console   -------------------------------------------

def wait_for_console():
  """ wait for serial connection """
  import supervisor
  import board
  import time
  while not supervisor.runtime.serial_connected:
    time.sleep(1)
  print(f"running on board {board.board_id}")

# --- connect to AP   --------------------------------------------------------

def connect():
  """ connect to AP with given ssid """

  from secrets import secrets
  import wifi
  print(f"connecting to AP {secrets['ssid']} ...")
  if 'timeout' in secrets:
    timeout = secrets['timeout']
  else:
    timeout = 5
  if 'retries' in secrets:
    retries = secrets['retries']
  else:
    retries = 3

  state = wifi.radio.connected
  print(f"  connected: {state}")
  if not state:
    for _ in range(retries):
      try:
        wifi.radio.connect(secrets['ssid'],
                           secrets['password'],
                           timeout = timeout
                           )
        break
      except ConnectionError as ex:
        print(f"{ex}")
    print(f"  connected: {wifi.radio.connected}")

# --- return generic position-map for displays   -----------------------------

def pos_map(display):
  """ return position-map for displays.
  This returns a tuple (anchor_point,anchored_position) for labels.
  """
  return {
    'NW': ((0.0,0.0),(0,               0)),
    'N':  ((0.5,0.0),(display.width/2, 0)),
    'NE': ((1.0,0.0),(display.width,   0)),
    'W':  ((0.0,0.5),(0,               display.height/2)),
    'C':  ((0.5,0.5),(display.width/2, display.height/2)),
    'E':  ((1.0,0.5),(display.width,   display.height/2)),
    'SW': ((0.0,1.0),(0,               display.height)),
    'S':  ((0.5,1.0),(display.width/2, display.height)),
    'SE': ((1.0,1.0),(display.width,   display.height)),
    }
