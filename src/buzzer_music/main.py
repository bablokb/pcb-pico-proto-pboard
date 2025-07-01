# ----------------------------------------------------------------------------
# Play a monophonic song.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-proto-pboard
# Website: https://github.com/bablokb/cp-buzzer-music
# ----------------------------------------------------------------------------

import time
import asyncio

from pboard import pboard
from buzzer_music.reader import MusicReader

async def main(notes):
  buzzer = pboard.buzzer()
  start = time.monotonic()
  for note in notes:
    delay = note[0] - (time.monotonic() - start)
    if delay > 0:
      await asyncio.sleep(delay)
    print(*note)
    await buzzer.tone(note[1],note[2])
  buzzer.deinit()
  pboard._buzzer = None

reader = MusicReader()
notes = reader.load(filename="Bach-Prelude-C-Dur.txt",bpm=120)
asyncio.run(main(notes))
