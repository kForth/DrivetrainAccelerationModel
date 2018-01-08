from collections import OrderedDict
from math import pi, radians, sin


class GenericModel:
    csv_headers = ['time(s)', 'dist(ft)', 'speed(ft/s)', 'accel(ft/s^2)', 'current(amps/10)', 'voltage',
                   'energy', 'total_energy', 'slip']

    def __init__(self,
                 motors,                        # Motor object
                 gear_ratio,                    # Gear ratio, driven/driving
                 motor_current_limit,           # Current limit per motor, A
                 effective_diameter,            # Effective diameter, in
                 effective_mass,                # Effective mass, lbs
                 k_gearbox_efficiency,          # Gearbox efficiency fraction
                 incline_angle,                 # Incline angle relative to ground, deg
                 check_for_slip,                # Check for slip or not
                 coeff_kinetic_friction,        # µk
                 coeff_static_friction,         # µs
                 k_resistance_s,                # static resistance, lbf
                 k_resistance_v,                # viscous resistance, lbf/(ft/s)
                 battery_voltage,               # Fully-charged open-circuit battery voltage
                 resistance_com,                # Resistance from bat to PDB (incl main breaker, Ω
                 resistance_one,                # Resistance from PDB to motor (incl PDB breaker), Ω
                 time_step,                     # Integration step size, s
                 simulation_time,               # Integration duration, s
                 max_dist):                     # Max distance to integrate to, ft

        self.motors = motors
        self.num_motors = self.motors.num_motors
        self.k_resistance_s = k_resistance_s
        self.k_resistance_v = k_resistance_v
        self.k_gearbox_efficiency = k_gearbox_efficiency
        self.gear_ratio = gear_ratio
        self.effective_diameter = effective_diameter
        self.effective_radius = effective_diameter * 0.5
        self.incline_angle = incline_angle
        self.effective_mass = effective_mass
        self.check_for_slip = check_for_slip
        self.coeff_kinetic_friction = coeff_kinetic_friction
        self.coeff_static_friction = coeff_static_friction
        self.motor_current_limit = motor_current_limit
        self.battery_voltage = battery_voltage
        self.resistance_com = resistance_com
        self.resistance_one = resistance_one
        self.time_step = time_step
        self.simulation_time = simulation_time
        self.max_dist = max_dist

        # calculate Derived Constants
        self.k_resistance_s *= 4.448222  # convert lbf to Newtons
        self.k_resistance_v *= 4.448222 * 3.28084  # convert lbf/(ft/s) to Newtons/(meter/sec)
        self.effective_radius = self.effective_radius * 2.54 / 100  # convert inches to meters
        self.effective_mass *= 0.4535924  # convert lbm to kg

        self.effective_weight = self.effective_mass * 9.80665  # effective weight, Newtons

        self.is_slipping = False  # state variable, init to false
        self.sim_time = 0  # elapsed time, seconds
        self.sim_distance = 0  # distance traveled, meters
        self.sim_speed = 0  # speed, meters/sec
        self.sim_acceleration = 0  # acceleration, meters/sec/sec
        self.sim_voltage = 0  # Voltage at the motor
        self.sim_current_per_motor = 0  # current per motor, amps
        self.sim_energy = 0  # power used, mAh
        self.cumulative_energy = 0  # total power used mAh

        self.data_points = []

    def reset(self):
        self.is_slipping = False  # state variable, init to false
        self.sim_time = 0  # elapsed time, seconds
        self.sim_distance = 0  # distance traveled, meters
        self.sim_speed = 0  # speed, meters/sec
        self.sim_acceleration = 0  # acceleration, meters/sec/sec
        self.sim_voltage = 0  # Voltage at the motor
        self.sim_current_per_motor = 0  # current per motor, amps

        self.data_points = []

    def _get_gravity_force(self):
        return self.effective_weight * sin(radians(self.incline_angle))

    def _calc_max_accel(self, velocity):  # compute acceleration w/ slip
        motor_speed = velocity / self.effective_radius * self.gear_ratio  # motor speed associated with pulley speed

        self.sim_current_per_motor = (self.sim_voltage - (motor_speed / self.motors.k_v)) / self.motors.k_r
        if velocity > 0 and self.motor_current_limit is not None:
                self.sim_current_per_motor = min(self.sim_current_per_motor, self.motor_current_limit)
        max_torque_at_voltage = self.motors.k_t * self.sim_current_per_motor

        max_torque_at_wheel = self.k_gearbox_efficiency * max_torque_at_voltage * self.gear_ratio  # available torque at wheels
        available_force_at_wheel = max_torque_at_wheel / self.effective_radius  # available force at wheels

        if self.check_for_slip:
            if available_force_at_wheel > self.effective_weight * self.coeff_static_friction:
                self.is_slipping = True
            elif available_force_at_wheel < self.effective_weight * self.coeff_kinetic_friction:
                self.is_slipping = False

        if self.check_for_slip and self.is_slipping:
            applied_force_at_wheel = (self.effective_weight * self.coeff_kinetic_friction)
        else:
            applied_force_at_wheel = available_force_at_wheel

        self.sim_voltage = self.battery_voltage - self.num_motors * self.sim_current_per_motor * self.resistance_com - \
                           self.sim_current_per_motor * self.resistance_one  # compute battery drain
        rolling_resistance = self.k_resistance_s + self.k_resistance_v * velocity  # rolling resistance, N
        net_accel_force = applied_force_at_wheel - rolling_resistance - self._get_gravity_force()  # Net force, N
        if net_accel_force < 0:
            net_accel_force = 0
        return net_accel_force / self.effective_mass

    def _integrate_with_heun(self):  # numerical integration using Heun's Method
        self.sim_time = self.time_step
        while self.sim_time < self.simulation_time + self.time_step and \
                (self.sim_distance * 3.28084 < self.max_dist or self.max_dist <= 0):
            v_temp = self.sim_speed + self.sim_acceleration * self.time_step  # kickstart with Euler step
            a_temp = self._calc_max_accel(v_temp)
            v_temp = self.sim_speed + (self.sim_acceleration + a_temp) / 2 * \
                                      self.time_step  # recalc v_temp trapezoidally
            self.sim_acceleration = self._calc_max_accel(v_temp)  # update a
            self.sim_distance += (self.sim_speed + v_temp) / 2 * self.time_step  # update x trapezoidally
            self.sim_speed = v_temp  # update V

            self.sim_energy = self.sim_current_per_motor * self.time_step * 1000 / 60 ** 2  # calc power usage in mAh
            self.cumulative_energy += self.sim_energy

            self._add_data_point()
            self.sim_time += self.time_step

    def _add_data_point(self):
        self.data_points.append(OrderedDict({
            'time':         self.sim_time,
            'pos':          self.sim_distance * 3.28084,
            'vel':          self.sim_speed * 3.28084,
            'accel':        self.sim_acceleration * 3.28084,
            'current':      self.sim_current_per_motor / 10,
            'voltage':      self.sim_voltage,
            'energy':       self.sim_energy,
            'total_energy': self.cumulative_energy,
            'is_slipping':  self.is_slipping
        }))

    def get_data_points(self):
        return self.data_points

    def get_final(self, key):
        return self.data_points[-1][key]

    def calc(self):
        self.sim_acceleration = self._calc_max_accel(self.sim_speed)  # compute accel at t=0
        self._add_data_point()  # output values at t=0

        self._integrate_with_heun()  # numerically integrate and output using Heun's method

    def to_json(self):
        return {

        }

    @staticmethod
    def from_json(data):
        temp = GenericModel.SAMPLE_CONFIG
        temp.update(data)
        return GenericModel(**temp)
