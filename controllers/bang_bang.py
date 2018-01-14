from controllers.control_loop import ControlLoop


class BangBangController(ControlLoop):
    def __init__(self):
        super().__init__()
        self.toggle_deadband = 0
        self.neutral_voltage = 0
        self.forward_voltage = 12
        self.reverse_voltage = -12

    def set_gains(self, toggle_deadband=0, neutral_voltage=0, forward_voltage=12, reverse_voltage=-12):
        self.toggle_deadband = toggle_deadband
        self.neutral_voltage = neutral_voltage
        self.forward_voltage = forward_voltage
        self.reverse_voltage = reverse_voltage

    def update(self, position, velocity, acceleration, voltage, current_per_motor):
        if position < (self._goal - self.toggle_deadband):
            return self.forward_voltage
        elif position > (self._goal + self.toggle_deadband):
            return self.reverse_voltage
        return self.neutral_voltage