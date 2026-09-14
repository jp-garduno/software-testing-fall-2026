from enum import Enum
from dataclasses import dataclass


class LightState(Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"
    PED_WALK = "Pedestrian Walk"
    PED_FLASH = "Pedestrian Flash"
    MAINTENANCE = "Maintenance"


@dataclass
class EventResult:
    success: bool
    message: str


class TrafficLight:
    def __init__(self):
        self.state = LightState.GREEN
        self.pedestrian_requested = False
        self.history = []

    def _transition(self, new_state):
        self.history.append((self.state, new_state))
        self.state = new_state

    # ------------------------
    # EVENTS
    # ------------------------

    def timer_green_expired(self):
        # ST_01
        if self.state == LightState.GREEN:
            self._transition(LightState.YELLOW)
            return EventResult(True, "Green → Yellow")

        # ST_23
        if self.state == LightState.MAINTENANCE:
            return EventResult(False, "System in maintenance.")

        # ST_11
        return EventResult(False, "Invalid event for current state.")

    def timer_yellow_expired(self):
        # ST_07 / ST_08
        if self.state == LightState.YELLOW:
            if self.pedestrian_requested:
                self.pedestrian_requested = False
                self._transition(LightState.PED_WALK)
                return EventResult(True, "Yellow → Pedestrian Walk")
            else:
                self._transition(LightState.RED)
                return EventResult(True, "Yellow → Red")

        # ST_04 / ST_15
        return EventResult(False, "Invalid event for current state.")

    def timer_red_expired(self):
        # ST_12
        if self.state == LightState.RED:
            self._transition(LightState.GREEN)
            return EventResult(True, "Red → Green")

        # ST_05
        return EventResult(False, "Invalid event for current state.")

    def pedestrian_button_pressed(self):
        # ST_02
        if self.state == LightState.GREEN:
            self.pedestrian_requested = True
            return EventResult(True, "Pedestrian request queued.")

        # ST_13
        if self.state == LightState.RED:
            self._transition(LightState.PED_WALK)
            return EventResult(True, "Pedestrian crossing activated.")

        # ST_24
        if self.state == LightState.MAINTENANCE:
            return EventResult(False, "System in maintenance.")

        # ST_09 / ST_17 / ST_21
        return EventResult(False, "Pedestrian request not allowed now.")

    def timer_walk_expired(self):
        # ST_16
        if self.state == LightState.PED_WALK:
            self._transition(LightState.PED_FLASH)
            return EventResult(True, "Walk → Flash")

        return EventResult(False, "Invalid event for current state.")

    def timer_flash_expired(self):
        # ST_19
        if self.state == LightState.PED_FLASH:
            self._transition(LightState.RED)
            return EventResult(True, "Flash → Red")

        return EventResult(False, "Invalid event for current state.")

    def enter_maintenance(self):
        # ST_25
        if self.state == LightState.MAINTENANCE:
            return EventResult(False, "Already in maintenance.")

        # ST_03, ST_10, ST_14, ST_18, ST_20
        self._transition(LightState.MAINTENANCE)
        return EventResult(True, "Entered maintenance mode.")

    def exit_maintenance(self):
        # ST_22
        if self.state == LightState.MAINTENANCE:
            self.pedestrian_requested = False
            self._transition(LightState.GREEN)
            return EventResult(True, "Exited maintenance.")

        # ST_06
        return EventResult(False, "Not in maintenance.")