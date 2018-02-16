from controllers.control_loop import ControlLoop


class FixedVoltageController(ControlLoop):
    def __init__(self):
        super().__init__()
        self._voltage = 0

    def set_gains(self, voltage):
        self._voltage = voltage

    def calc_voltage(self, position):
        return self._voltage
