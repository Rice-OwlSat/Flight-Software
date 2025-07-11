from Tasks.template_task import Task
import board
from analogio import AnalogIn

class task(Task):
    priority = 10
    frequency = 1
    name = 'euv'
    color = 'red'

    schedule_later = True

    async def main_task(self):
        # take EUV readings
        readings = {
            'EUV_x': (AnalogIn(board.A1).value * 3.3) / 65536,
            'EUV_y': 0,
            'EUV_z': 0,
        }

        # store them in our cubesat data_cache object
        self.cubesat.data_cache.update({'euv':readings})

        # print the readings with some fancy formatting
        self.debug('EUV reading')
        for euv_type in self.cubesat.data_cache['euv']:
            self.debug('{:>5} {}'.format(euv_type,self.cubesat.data_cache['euv'][euv_type]),2)
