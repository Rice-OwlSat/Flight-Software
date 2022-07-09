# Task to obtain IMU sensor readings

from Tasks.template_task import Task

class task(Task):
    priority = 5
    frequency = 1/10 # once every 10s
    name='imu'
    color = 'green'

    async def main_task(self):
        if self.cubesat.data_cache["task_flags"]["collect_imu_data"] == True:
            # Take IMU readings
            readings = {
                'accel':self.cubesat.acceleration,
                'mag':  self.cubesat.magnetic,
                'gyro': self.cubesat.gyro,
            }

            # Store them in our cubesat data_cache object
            self.cubesat.data_cache.update({'imu':readings})

            # Print the readings with some fancy formatting
            self.debug('IMU readings (x,y,z)')
            for imu_type in self.cubesat.data_cache['imu']:
                self.debug('{:>5} {}'.format(imu_type,self.cubesat.data_cache['imu'][imu_type]),2)



