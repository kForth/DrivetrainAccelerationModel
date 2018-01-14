class ControlLoop:
    def __init__(self):
        self._goal = 0
        self._deadband = 0
        self._last_error = 0

    def reset(self):
        self._last_error = 0

    def get_error(self):
        return self._last_error

    def set_deadband(self, deadband):
        self._deadband = deadband

    def set_goal(self, goal):
        self._goal = goal

    def is_done(self, position):
        return abs(position - self._goal) < self._deadband

    def set_gains(self, *args, **kwargs):
        pass

    def update(self, position, velocity, acceleration, voltage, current_per_motor):
        return 0
