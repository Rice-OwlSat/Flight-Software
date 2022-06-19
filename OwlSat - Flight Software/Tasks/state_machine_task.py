# Task to manage satellite state machine

from Tasks.template_task import Task
import state_machine

SM = state_machine.StateMachine()

class task(Task):
    priority = 1
    frequency = 2 # 2 times per second
    name = 'state_machine'
    color = 'red'

    async def main_task(self):
        # Iterate SM and get task flags:
        flags = SM.iterate()

        # Update task flags in the cubesat data_cache object
        self.cubesat.data_cache.update({'task_flags':flags})

        # DEBUG: Print the resulting flag states:
        self.debug('STATE MACHINE - Task Flags:')
        for flag in self.cubesat.data_cache['task_flags']:
            self.debug('{:>5} {}'.format(flag, self.cubesat.data_cache['task_flags'][flag]), 2)