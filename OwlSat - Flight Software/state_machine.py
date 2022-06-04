import asyncio
from pycubed import *

# State ID Constants
STOWED = 0
DEPLOYED = 1
DETUMBLING = 2
STABLE = 3
MISSION = 4
RECOVERY = -1

DEPLOYED_TASKS = ()
DETUMBLING_TASKS = ()
STABLE_TASKS = ()
MISSION_TASKS = ()
RECOVERY_TASKS = ()

ALL_TASKS = ()


def cancel_all_tasks():
    for task in asyncio.Task.all_tasks():
        if not task.done():
            task.cancel()


class StateMachine:
    def __init__(self, all_tasks=tuple([])):
        # set of flags used to check for state advancement
        self.state = STOWED

        self._inhibit_switches_triggered = False
        self._deployment_successful = False
        self._angular_velocity_stable = False
        self._battery_check_successful = False
        self._ground_station_link_successful = False

        self._task_enable = dict([])

        for task in all_tasks:
            self._task_enable[task] = False

    def reset_tasks(self):
        for task in self._task_enable.keys():
            self._task_enable[task] = False

    def update_tasks(self):
        self.reset_tasks()

        if self.state == STOWED:
            pass

        elif self.state == DEPLOYED:
            for task in DEPLOYED_TASKS:
                self._task_enable[task] = True

        elif self.state == DETUMBLING:
            for task in DETUMBLING_TASKS:
                self._task_enable[task] = True

        elif self.state == STABLE:
            for task in STABLE_TASKS:
                self._task_enable[task] = True

        elif self.state == MISSION:
            for task in MISSION_TASKS:
                self._task_enable[task] = True

        elif self.state == RECOVERY:
            for task in RECOVERY_TASKS:
                self._task_enable[task] = True

    def progress_state(self):
        if self.state == STOWED and self._inhibit_switches_triggered:
            ### TURN ON CUBESAT POWER
            cubesat.reinit() ## CHECK LATER

            self.state = DEPLOYED

        elif self.state = DEPLOYED:
            # cubesat.burn() ## CHECK LATER

            if self._deployment_successful:
                self.state = DETUMBLING
            else:
                self.state = RECOVERY

        elif self.state = DETUMBLING:
            if self._angular_velocity_stable and self._battery_check_successful:
                self.state = MISSION
            elif not self._battery_check_successful:
                self.state = RECOVERY

        elif self.state = MISSION:
            if self._battery_check_successful and self._ground_station_link_successful and self._angular_velocity_stable:
                pass
            else:
                self.state = RECOVERY



# class State:
#     id = None
#     name = None
#
#     def __init__(self, tasks=tuple([])):
#
#         self._tasks = [task for task in tasks]
#
#     def __repr__(self):
#         return self.name + "-" + str(self.id)
#
#     def sort_tasks(self):
#         self._tasks.sort(key=lambda x: x.priority)
#
#     def add_task(self, new_task):
#         self._tasks.append(new_task)
#
#     async def initial_tasks(self):
#         return
#
#     async def run_checks(self):
#         return
#
#     async def queue_tasks(self):
#         for task in self._tasks:
#             asyncio.create_task(task.main_task())
#
# class Stowed(State):
#     id = 0
#     name = "Stowed"
#
#     async def progress_state(self):
#         cubesat.powermode('norm')
#
#         return Deployed()
#
# class Deployed(State):
#     id = 1
#     name = "Deployed"
#
#     async def initial_tasks(self):
#         ## How to initialize IO?
#         ## It seems like the external modules are already initialized in __init__ for cubesat
#         cubesat.reinit()
#         cubesat.burn()
#
#     def progress_state(self):
#
#         if # satellite deployment successful
#
#         return Detumbling()
#
# class Detumbling(State):
#     id = 2
#     name = "Detumbling"
#
#     def progress_state




