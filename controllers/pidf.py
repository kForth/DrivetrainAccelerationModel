from controllers.control_loop import ControlLoop


class PidfController(ControlLoop):
    def __init__(self):
        super().__init__()
        self.k_f = 0
        self.k_p = 0
        self.k_i = 0
        self.k_d = 0
        self._min_i_error = 0.1
        self._error_sum = 0

    def reset(self):
        super().reset()
        self._error_sum = 0

    def set_gains(self, k_f=0, k_p=0, k_i=0, k_d=0, min_i_error=0.1):
        self.k_f = k_f
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self._min_i_error = min_i_error

    def update(self, position, velocity, acceleration, voltage, current_per_motor):
        error = self._goal - position

        if abs(error) < self._min_i_error:
            self._error_sum += error

        p = self.k_p * error
        i = (self.k_i * self._error_sum)
        d = self.k_d * (error - self._last_error)
        f = self.k_f * self._goal

        # if (error > 0 and self._last_error < 0) or (error < 0 and self._last_error > 0):
        #     i = 0
        #     self._error_sum = 0

        self._last_error = error
        return p + i - d + f
