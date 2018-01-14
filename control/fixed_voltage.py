from control.control_loop import ControlLoop


class FixedVoltageController(ControlLoop):
    def __init__(self):
        super().__init__()
        self._voltage = 0

    def set_gains(self, voltage):
        self._voltage = voltage

    def update(self, position, velocity, acceleration, voltage, current_per_motor):
        return self._voltage
