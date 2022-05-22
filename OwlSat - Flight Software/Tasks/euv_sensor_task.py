from Tasks.template_task import Task
import board
from analogio import AnalogIn

SENSOR1_PIN = board.A0
SENSOR2_PIN = board.A1
SENSOR3_PIN = board.A2
SENSOR4_PIN = board.A4
SENSOR5_PIN = board.A5

class task(Task):
    priority = 10
    frequency = 3
    name = 'euv'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        # take EUV readings
        readings = {
            'EUV_+x': (AnalogIn(SENSOR1_PIN).value * 3.3) / 65536,
            'EUV_-x': (AnalogIn(SENSOR2_PIN).value * 3.3) / 65536,
            'EUV_+y': (AnalogIn(SENSOR3_PIN).value * 3.3) / 65536,
            'EUV_-y': (AnalogIn(SENSOR4_PIN).value * 3.3) / 65536,
            'EUV_+z': (AnalogIn(SENSOR5_PIN).value * 3.3) / 65536
        }

        # store them in our cubesat data_cache object
        self.cubesat.data_cache.update({'euv':readings})

        # print the readings with some fancy formatting
        self.debug('EUV reading')
        for euv_type in self.cubesat.data_cache['euv']:
            self.debug('{:>5} {}'.format(euv_type,self.cubesat.data_cache['euv'][euv_type]),2)
