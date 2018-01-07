from math import pi


class Motor(object):
    max_voltage = 12   # Volts
    free_rpm = 1       # RPM
    stall_torque = 1   # in*oz
    stall_current = 1  # Amps
    free_current = 1   # Amps

    def __init__(self, num_motors=1):
        self.num_motors = num_motors
        self.free_speed = self.free_rpm * 2 * pi / 60  # convert RPM to rad/sec
        self.k_r = self.max_voltage / self.stall_current
        self.k_v = self.free_speed / (self.max_voltage - self.k_r * self.free_current)
        self.k_t = self.num_motors * self.stall_torque / self.stall_current

    def to_json(self):
        return {
            'max_voltage':   self.max_voltage,
            'free_speed':    self.free_speed / (2 * 3.1415926536 / 60),
            'stall_torque':  self.stall_torque,
            'stall_current': self.stall_current,
            'free_current': self.free_current
        }


class CIM(Motor):
    max_voltage = 12
    free_rpm = 5330
    stall_torque = 2.41
    stall_current = 131
    free_current = 2.7


class MiniCIM(Motor):
    max_voltage = 12
    free_rpm = 5840
    stall_torque = 1.41
    stall_current = 89
    free_current = 3


class BAG(Motor):
    max_voltage = 12
    free_rpm = 13180
    stall_torque = 0.43
    stall_current = 53
    free_current = 1.8


class _775pro(Motor):
    max_voltage = 12
    free_rpm = 18730
    stall_torque = 0.71
    stall_current = 134
    free_current = 0.7


class AM_9015(Motor):
    max_voltage = 12
    free_rpm = 14270
    stall_torque = 0.36
    stall_current = 71
    free_current = 3.7


class AM_NeveRest(Motor):
    max_voltage = 12
    free_rpm = 5480
    stall_torque = 0.17
    stall_current = 10
    free_current = 0.4


class AM_RS775_125(Motor):
    max_voltage = 12
    free_rpm = 5800
    stall_torque = 0.28
    stall_current = 18
    free_current = 1.6


class BB_RS_775_18V(Motor):
    max_voltage = 12
    free_rpm = 13050
    stall_torque = 0.72
    stall_current = 97
    free_current = 2.7


class BB_RS_550(Motor):
    max_voltage = 12
    free_rpm = 19000
    stall_torque = 0.38
    stall_current = 84
    free_current = 0.4

MOTOR_LOOKUP = {
    'cim': CIM,
    'minicim': MiniCIM,
    'bag': BAG,
    '775pro': _775pro,
    'am9015': AM_9015,
    'amneverrest': AM_NeveRest,
    'amrs775125': AM_RS775_125,
    'bbrs77518v': BB_RS_775_18V,
    'bbrs550': BB_RS_550
}