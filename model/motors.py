class Motor(object):
    max_voltage = 1  # Volts
    free_speed = 1  # RPM
    stall_torque = 1  # in*oz
    stall_current = 1  # Amps

    def __init__(self):
        self.free_speed *= 2 * 3.1415926536 / 60  # convert RPM to rad/sec

    def to_json(self):
        return {
            'max_voltage': self.max_voltage,
            'free_speed': self.free_speed / (2 * 3.1415926536 / 60),
            'stall_torque': self.stall_torque,
            'stall_current': self.stall_current
        }


class CIM(Motor):
    max_voltage = 12
    free_speed = 5330
    stall_torque = 2.41
    stall_current = 131


class MiniCIM(Motor):
    max_voltage = 12
    free_speed = 5840
    stall_torque = 1.41
    stall_current = 89


class BAG(Motor):
    max_voltage = 12
    free_speed = 13180
    stall_torque = 0.43
    stall_current = 53


class _775pro(Motor):
    max_voltage = 12
    free_speed = 18730
    stall_torque = 0.71
    stall_current = 134


class AM_9015(Motor):
    max_voltage = 12
    free_speed = 14270
    stall_torque = 0.36
    stall_current = 71


class AM_NeveRest(Motor):
    max_voltage = 12
    free_speed = 5480
    stall_torque = 0.17
    stall_current = 10


class AM_RS775_125(Motor):
    max_voltage = 12
    free_speed = 5800
    stall_torque = 0.28
    stall_current = 18


class BB_RS_775_18V(Motor):
    max_voltage = 12
    free_speed = 13050
    stall_torque = 0.72
    stall_current = 97


class BB_RS_550(Motor):
    max_voltage = 12
    free_speed = 19000
    stall_torque = 0.38
    stall_current = 84

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