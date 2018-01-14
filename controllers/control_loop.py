from abc import abstractmethod


class ControlLoop:


    def __init__(self):
        self._goal = 0
        self._deadband = 0
        self._last_error = 0
        self._on_goal = False

    def reset(self):
        self._last_error = 0
        self._on_goal = False

    def get_goal(self):
        return self._goal

    def get_error(self):
        return self._last_error

    def set_deadband(self, deadband):
        self._deadband = deadband

    def set_goal(self, goal):
        self._goal = goal

    def is_done(self):
        return self._on_goal

    def set_gains(self, *args, **kwargs):
        pass

    @abstractmethod
    def calc_voltage(self, position, velocity, acceleration, voltage, current_per_motor):
        return 0

    def update(self, position, velocity, acceleration, voltage, current_per_motor):
        self._error = self._goal - position
        voltage = self.calc_voltage(position, velocity, acceleration, voltage, current_per_motor)
        self._last_error = self._error
        self._on_goal = abs(self._last_error) < self._deadband
        return voltage

    def get_data_point(self):
        return {
            'error': self._last_error,
            'goal': self._goal,
            'done': 1 if self._on_goal else 0
        }
