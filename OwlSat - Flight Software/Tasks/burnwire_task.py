# Trigger the burnwire antenna deployment

from Tasks.template_task import Task
from pycubed import cubesat

"""
Burn wire is triggered by activating the burnwire circuit for 1 second using a 1kHz 15% duty cycle PWM current flow
"""

class task(Task):
    priority = 255
    frequency = 0.2 # Once every five seconds - 1s on, 4s off
    name = 'burnwire'
    color = 'orange'

    async def main_task(self):
        if self.cubesat.data_cache["task_flags"]["deploy_antenna"] == True:
            # CURRENTLY SET TO USE BURNWIRE #1 (To change this to burnwire 2 replace burn_num with ='2')
            cubesat.burn(burn_num='1', dutycycle=0.15, duration=1)
