# State ID Constants
STOWED = 0
DEPLOYING = 1
DETUMBLING = 2
STABLE = 3
MISSION = 4
RECOVERY = -1

TASK_SETS = {DEPLOYING: ["deploy_antenna"],
            DETUMBLING: ["poll_power_status",
                         "collect_imu_data",
                         "update_magnetorquer_command"],
                STABLE: ["poll_power_status",
                         "collect_imu_data",
                         "update_magnetorquer_command",
                         "transmit_data"],
               MISSION: ["poll_power_status",
                         "collect_imu_data",
                         "collect_solar_data",
                         "collect_gps_data",
                         "collect_euv_data",
                         "compute_orientation",
                         "update_magnetorquer_command",
                         "transmit_data",
                         "write_cache_to_SD"],
              RECOVERY: ["update_power_bus",
                         "poll_power_status"]}

ALL_TASKS = ["collect_imu_data",
             "collect_solar_data",
             "collect_gps_data",
             "collect_euv_data",
             "compute_orientation",
             "poll_power_status",
             "update_power_bus",
             "update_magnetorquer_command",
             "transmit_data",
             "deploy_antenna"
             "write_cache_to_SD"]


class StateMachine:
    def __init__(self):
        self.state = STOWED
        self.deployment_successful = False
        self.angular_velocity_stable = False
        self.battery_check_successful = False
        self.ground_station_link_successful = False
        self.task_flags = {
                          "poll_power_status": False,
                          "update_power_bus" : False,
                           "collect_imu_data": False,
                         "collect_solar_data": False,
                           "collect_gps_data": False,
                           "collect_euv_data": False,
                        "compute_orientation": False,
                "update_magnetorquer_command": False,
                              "transmit_data": False,
                             "deploy_antenna": False,
                          "write_cache_to_SD": False}

    def reset_tasks(self):
        for task in self.task_flags.keys():
            self.task_flags[task] = False

    def update_tasks(self):
        self.reset_tasks()

        if self.state != STOWED:
            for task in TASK_SETS[self.state]:
                self.task_flags[task] = True

    def progress_state(self):
        if self.state == STOWED: # Cubesat just turned ON
            self.state = DEPLOYING

        elif self.state == DEPLOYING: # Cubesat is initialized and running - Antenna must be deployed
            if self.deployment_successful:
                self.state = DETUMBLING
            elif not self.deployment_successful:
                self.state = DEPLOYING

        elif self.state == DETUMBLING: # Cubesat is detumbling
            if self.angular_velocity_stable:
                self.state = STABLE
            elif not self.angular_velocity_stable:
                self.state = DETUMBLING

        elif self.state == STABLE: # Cubesat has detumbled - Must establish comms link
            if self.angular_velocity_stable and self.battery_check_successful and self.ground_station_link_successful:
                self.state = MISSION
            elif not self.battery_check_successful:
                self.state = RECOVERY
            elif not self.angular_velocity_stable:
                self.state = DETUMBLING
            elif not self.ground_station_link_successful:
                self.state = STABLE

        elif self.state == MISSION: # Cubesat is performing mission
            if self.angular_velocity_stable and self.battery_check_successful and self.ground_station_link_successful:
                self.state = MISSION
            elif not self.battery_check_successful:
                self.state = RECOVERY
            elif not self.angular_velocity_stable:
                self.state = DETUMBLING
            elif not self.ground_station_link_successful:
                self.state = STABLE

        elif self.state == RECOVERY:
            pass

    def get_flags(self):
        return self.task_flags

    def iterate(self):
        self.progress_state()
        self.update_tasks()
        return self.get_flags()