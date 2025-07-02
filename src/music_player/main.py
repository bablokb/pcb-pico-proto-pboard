# ----------------------------------------------------------------------------
# Play MP3-files from the SD-card
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-pboard
# ----------------------------------------------------------------------------

import audiomp3
import os
import time

from pboard import pboard

class Player:
  """ Audio-Controller """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._files = []
    self._audio, self._mute = pboard.i2s()
    self._btn = pboard.button(0)
    pboard.mount_sd()
    self._file_list()

  # --- read list of music-files   ---------------------------------------------

  def _file_list(self):
    """ read list of mp3-files """

    try:
      files = os.listdir("/sd")
      self._files = ["/sd/"+f for f in files if f[-3:] == "mp3"]
      self._files.sort()
      print(f"{self._files=}")
    except Exception as ex:
      print(f"failed reading SD-card: {ex}")
      self._files = []

  # --- play music   -----------------------------------------------------------

  def play(self):
    """ play music """

    print("start playing music")
    for f in self._files:
      try:
        fstream = open(f,"rb")
        mp3 = audiomp3.MP3Decoder(fstream)
        print(f"starting {f}")
        self.mute(False)
        self._audio.play(mp3)
        while self._audio.playing:
          if not self._btn.value:
            print("toggling mute")
            self.mute()
            time.sleep(0.2)
        print(f"finished playing {f}")
      except Exception as ex:
        print(f"could not play {f}: {ex}")
      fstream.close()
      mp3.deinit()

  # --- mute   ---------------------------------------------------------------

  def mute(self, value = None):
    """ drive mute-pin """
    if value is None:
      # toggle mute
      self._mute.value = not self._mute.value
    else:
      # we want to unmute if mute==False
      self._mute.value = not value

# --- main program   ---------------------------------------------------------

player = Player()
player.play()
