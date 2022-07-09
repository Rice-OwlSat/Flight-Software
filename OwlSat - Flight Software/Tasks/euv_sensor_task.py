from Tasks.template_task import Task
import board
from analogio import AnalogIn
from pycubed import cubesat
import os, storage, time
import busio
import digitalio
import adafruit_sdcard
import storage


SENSOR1_PIN = board.A0
SENSOR2_PIN = board.A1
SENSOR3_PIN = board.A2
SENSOR4_PIN = board.A4
SENSOR5_PIN = board.A5

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.SD_CS)

sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)

storage.mount(vfs, "/sd")

class task(Task):
    priority = 10
    frequency = 3
    name = 'euv'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        if self.cubesat.data_cache["task_flags"]["collect_euv_data"] == True:
            # Take EUV readings
            readings = {
                'EUV_+x': (AnalogIn(SENSOR1_PIN).value * 3.3) / 65536,
                'EUV_-x': (AnalogIn(SENSOR2_PIN).value * 3.3) / 65536,
                'EUV_+y': (AnalogIn(SENSOR3_PIN).value * 3.3) / 65536,
                'EUV_-y': (AnalogIn(SENSOR4_PIN).value * 3.3) / 65536,
                'EUV_+z': (AnalogIn(SENSOR5_PIN).value * 3.3) / 65536
            }

            # Store them in our cubesat data_cache object
            self.cubesat.data_cache.update({'euv':readings})

            # Also store them in the SD card:
            with open("/sd/test.txt", "w") as f:
                f.write(self.cubesat.data_cache['euv'])

            # Print the readings with some fancy formatting
            self.debug('EUV reading')
            for euv_type in self.cubesat.data_cache['euv']:
                self.debug('{:>5} {}'.format(euv_type,self.cubesat.data_cache['euv'][euv_type]),2)
