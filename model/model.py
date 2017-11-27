from model.motors import MOTOR_LOOKUP


class Model:
    CONFIG_KEYS = ['motor_type', 'num_motors', 'k_rolling_resistance_s', 'k_rolling_resistance_v',
                   'k_drivetrain_efficiency', 'gear_ratio', 'wheel_radius', 'vehicle_mass',
                   'coeff_kinetic_friction', 'coeff_static_friction', 'battery_voltage',
                   'resistance_com', 'resistance_one', 'time_step', 'simulation_time']

    SAMPLE_CONFIG = {
        'motor_type':              'CIM',  # type of motor (CIM, MiniCIM, BAG, _775pro, AM_9015, AM_NeveRest, AM_RS775_125, BB_RS_775_18V, BB_RS_5)
        'num_motors':              4,  # number of motors

        'k_rolling_resistance_s':  10,  # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,  # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_drivetrain_efficiency': 0.7,  # drivetrain efficiency fraction

        'gear_ratio':              12.75,  # gear ratio
        'wheel_radius':            3,  # wheel radius, inches

        'vehicle_mass':            150,  # vehicle mass, lbm
        'coeff_kinetic_friction':  0.8,  # coefficient of kinetic friction
        'coeff_static_friction':   1.0,  # coefficient of static friction

        'battery_voltage':         12.7,  # fully-charged open-circuit battery volts

        'resistance_com':          0.013,  # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':          0.002,  # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':               0.001,  # integration step size, seconds
        'simulation_time':         100,  # integration duration, seconds
        'max_dist':                15  # max distance to integrate to, feet
    }

    def __init__(self, motor_type, num_motors, k_rolling_resistance_s, k_rolling_resistance_v, k_drivetrain_efficiency,
                 gear_ratio, wheel_radius, vehicle_mass, coeff_kinetic_friction, coeff_static_friction, battery_voltage,
                 resistance_com, resistance_one, time_step, simulation_time, max_dist):
        self.motor_type = motor_type
        self.motor = MOTOR_LOOKUP[motor_type.lower().replace(' ', '').replace('_', '')]()
        self.num_motors = num_motors
        self.k_rolling_resistance_s = k_rolling_resistance_s
        self.k_rolling_resistance_v = k_rolling_resistance_v
        self.k_drivetrain_efficiency = k_drivetrain_efficiency
        self.gear_ratio = gear_ratio
        self.wheel_radius = wheel_radius
        self.vehicle_mass = vehicle_mass
        self.coeff_kinetic_friction = coeff_kinetic_friction
        self.coeff_static_friction = coeff_static_friction
        self.battery_voltage = battery_voltage
        self.resistance_com = resistance_com
        self.resistance_one = resistance_one
        self.time_step = time_step
        self.simulation_time = simulation_time
        self.max_dist = max_dist
        self.config_backup = dict([(e, self.__dict__[e]) for e in Model.CONFIG_KEYS])

        # calculate Derived Constants
        self.convert_units_to_si()

        self.torque_offset = (self.motor.stall_torque * self.battery_voltage * self.motor.free_speed) / (
            self.motor.max_voltage * self.motor.free_speed + self.motor.stall_current * self.resistance_one * self.motor.free_speed + self.motor.stall_current * self.num_motors * self.resistance_com * self.motor.free_speed)
        self.torque_slope = (self.motor.stall_torque * self.motor.max_voltage) / (
            self.motor.max_voltage * self.motor.free_speed + self.motor.stall_current * self.resistance_one * self.motor.free_speed + self.motor.stall_current * self.num_motors * self.resistance_com * self.motor.free_speed)
        self.k_t = self.motor.stall_torque / self.motor.stall_current
        self.force_to_amps = self.wheel_radius / (
            self.num_motors * self.k_drivetrain_efficiency * self.gear_ratio * self.k_t)  # vehicle total force to per-motor amps conversion
        self.vehicle_weight = self.vehicle_mass * 9.80665  # vehicle weight, Newtons

        self.is_slipping = False  # state variable, init to false
        self.sim_voltage = 0  # Voltage at the motor
        self.sim_speed = 0  # vehicle speed, meters/sec
        self.sim_distance = 0  # vehicle distance traveled, meters
        self.sim_time = 0  # elapsed time, seconds
        self.sim_acceleration = 0  # vehicle acceleration, meters/sec/sec
        self.sim_current_per_motor = 0  # current per motor, amps

        self.csv_lines = []

    def convert_units_to_si(self):
        self.k_rolling_resistance_s *= 4.448222  # convert lbf to Newtons
        self.k_rolling_resistance_v *= 4.448222 * 3.28083  # convert lbf/(ft/s) to Newtons/(meter/sec)
        self.wheel_radius = self.wheel_radius * 2.54 / 100  # convert inches to meters
        self.vehicle_mass *= 0.4535924  # convert lbm to kg

    def calc_max_accel(self, wheel_speed):  # compute acceleration w/ slip
        motor_speed = wheel_speed / self.wheel_radius * self.gear_ratio  # motor speed associated with vehicle speed
        max_torque_at_voltage = self.torque_offset - self.torque_slope * motor_speed  # available torque at motor @ V, in Newtons
        max_torque_at_wheel = self.k_drivetrain_efficiency * max_torque_at_voltage * self.gear_ratio  # available torque at wheels
        available_force_at_wheel = max_torque_at_wheel / self.wheel_radius * self.num_motors  # available force at wheels
        if available_force_at_wheel > self.vehicle_weight * self.coeff_static_friction:
            self.is_slipping = True
        elif available_force_at_wheel < self.vehicle_weight * self.coeff_kinetic_friction:
            self.is_slipping = False
        applied_force_at_wheel = (self.vehicle_weight * self.coeff_kinetic_friction) if self.is_slipping else available_force_at_wheel
        self.sim_current_per_motor = applied_force_at_wheel * self.force_to_amps  # computed here for output
        self.sim_voltage = self.battery_voltage - self.num_motors * self.sim_current_per_motor * self.resistance_com - self.sim_current_per_motor * self.resistance_one  # computed here for output
        rolling_resistance = self.k_rolling_resistance_s + self.k_rolling_resistance_v * wheel_speed  # rolling resistance force, in Newtons
        net_accel_force = applied_force_at_wheel - rolling_resistance  # net force available for acceleration, in Newtons
        if net_accel_force < 0:
            net_accel_force = 0
        return net_accel_force / self.vehicle_mass

    def integrate_with_heun(self):  # numerical integration using Heun's Method
        self.sim_time = self.time_step
        while self.sim_time < self.simulation_time + self.time_step and (self.sim_distance * 3.28083 < self.max_dist or self.max_dist <= 0):
            v_temp = self.sim_speed + self.sim_acceleration * self.time_step  # kickstart with Euler step
            a_temp = self.calc_max_accel(v_temp)
            v_temp = self.sim_speed + (
                                          self.sim_acceleration + a_temp) / 2 * self.time_step  # recalc v_temp trapezoidally
            self.sim_acceleration = self.calc_max_accel(v_temp)  # update a
            self.sim_distance += (self.sim_speed + v_temp) / 2 * self.time_step  # update x trapezoidally
            self.sim_speed = v_temp  # update V
            self.add_csv_line()
            self.sim_time += self.time_step

    # for reference only not used:
    def integrate_with_euler(self):  # numerical integration using Euler's Method
        self.sim_time = self.time_step
        while self.sim_time < self.simulation_time + self.time_step \
                and (self.sim_distance * 3.28083 < self.max_dist or self.max_dist <= 0):
            self.sim_speed += self.sim_acceleration * self.time_step
            self.sim_distance += self.sim_speed * self.time_step
            self.sim_acceleration = self.calc_max_accel(self.sim_speed)
            self.add_csv_line()
            self.sim_time += self.time_step

    def add_csv_line(self):
        self.csv_lines.append([self.sim_time, self.sim_distance * 3.28083, self.sim_speed * 3.28083,
                               self.is_slipping, self.sim_acceleration * 3.28083,
                               self.num_motors * self.sim_current_per_motor / 10,
                               self.sim_voltage])

    def calc(self):
        self.csv_lines.append(['t', 'feet', 'ft/s', 'slip', 'ft/s^2', 'amps/10', 'V'] +
                              [e + "=" + str(self.config_backup[e]) for e in self.config_backup.keys()])

        self.sim_acceleration = self.calc_max_accel(self.sim_speed)  # compute accel at t=0
        self.add_csv_line()  # output values at t=0

        self.integrate_with_heun()  # numerically integrate and output using Heun's method

    def get_csv_str(self):
        return "\n".join([",".join([str(format(e, '.5f') if isinstance(e, float) else e) for e in line]) for line in self.csv_lines])

    def print_csv(self):
        print(self.get_csv_str())

    def save_csv(self, filename):
        open(filename, "w+").write(self.get_csv_str())

    def to_json(self):
        return self.config_backup

    @staticmethod
    def from_json(data):
        return Model(**data) if all([k in data.keys() for k in Model.CONFIG_KEYS]) else None
