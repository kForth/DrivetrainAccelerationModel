from collections import OrderedDict

from model import CustomModel


class IntakeShooterModel(CustomModel):

    def __init__(self,
                 motors,  # Motor object
                 gear_ratio,  # Gear ratio, driven/driving
                 wheel_diameter,  # Effective diameter, m
                 element_mass,  # Game element mass, kg
                 compression_force,  # Compression force, N
                 incline_angle=0,
                 motor_current_limit=None,
                 motor_peak_current_limit=None,
                 motor_voltage_limit=None,
                 coeff_kinetic_friction=0.8,
                 coeff_static_friction=1.0,
                 k_gearbox_efficiency=0.85,
                 k_resistance_s=0,
                 k_resistance_v=0,
                 battery_voltage=12.5,
                 resistance_com=0.013,
                 resistance_one=0.002,
                 time_step=0.005,
                 simulation_time=10.0,
                 check_for_slip=True,
                 controller=None,
                 auto_calc=True,
                 name=None):
        self.compression_force = compression_force
        super().__init__(motors, gear_ratio, motor_current_limit, motor_peak_current_limit, motor_voltage_limit,
                         wheel_diameter, element_mass, k_gearbox_efficiency, incline_angle, check_for_slip,
                         coeff_kinetic_friction, coeff_static_friction, k_resistance_s, k_resistance_v, battery_voltage,
                         resistance_com, resistance_one, time_step, simulation_time, None, 0, 0, 0,
                         controller, auto_calc, name)

    def _calc_max_accel(self, velocity):
        motor_speed = velocity / self.effective_radius * self.gear_ratio

        available_voltage = self._voltage
        if self.motor_voltage_limit:
            available_voltage = min(self._voltage, self.motor_voltage_limit)
        applied_voltage = min(self._voltage_setpoint, available_voltage)

        self._current_per_motor = (applied_voltage - (motor_speed / self.motors.k_v)) / self.motors.k_r

        if velocity > 0 and self.motor_current_limit is not None:
            if (sum(self._current_history) / len(self._current_history)) \
                    > self.motor_current_limit or self._was_current_limited:
                self._was_current_limited = True
                self._current_per_motor = min(self._current_per_motor, self.motor_current_limit)
        if self.motor_peak_current_limit is not None:
            self._current_per_motor = min(self._current_per_motor, self.motor_peak_current_limit)

        max_torque_at_voltage = self.motors.k_t * self._current_per_motor

        available_torque_at_axle = self.k_gearbox_efficiency * max_torque_at_voltage * self.gear_ratio
        available_force_at_axle = available_torque_at_axle / self.effective_radius

        if self.check_for_slip:
            if available_force_at_axle > self.compression_force * self.coeff_static_friction:
                self._slipping = True
            elif available_force_at_axle < self.compression_force * self.coeff_kinetic_friction:
                self._slipping = False

            if self._slipping:
                available_force_at_axle = (self.compression_force * self.coeff_kinetic_friction)

        self._voltage = self.battery_voltage - (self._current_per_motor * self.resistance_one) - \
                        (self.num_motors * self._current_per_motor * self.resistance_com)

        self._brownout = self._voltage < self.BROWNOUT_VOLTAGE

        tuned_resistance = self.k_resistance_s + self.k_resistance_v * velocity  # rolling resistance, N
        net_accel_force = available_force_at_axle - tuned_resistance - self._get_gravity_force()  # Net force, N

        if net_accel_force < 0 and self._position <= 0:
            net_accel_force = 0
        return net_accel_force / self.effective_mass

    def _integrate_with_heun(self):  # numerical integration using Heun's Method
        self._time = self.time_step
        while self._time < self.simulation_time + self.time_step and \
                (self._position < self.max_dist or not self.max_dist):
            self.update()
            v_temp = self._velocity + self._acceleration * self.time_step  # kickstart with Euler step
            a_temp = self._calc_max_accel(v_temp)
            v_temp = self._velocity + (self._acceleration + a_temp) / 2 * \
                                      self.time_step  # recalc v_temp trapezoidally
            self._position += (self._velocity + v_temp) / 2 * self.time_step  # update x trapezoidally
            self._velocity = v_temp  # update V
            self._acceleration = self._calc_max_accel(v_temp)  # update a

            self._energy_per_motor = self._current_per_motor * self.time_step * 1000 / 60 / 60  # calc power usage in mAh
            self._cumulative_energy += self._energy_per_motor * self.num_motors
            self._current_history.append(self._current_per_motor)
            if len(self._current_history) > self._current_history_size:
                self._current_history = self._current_history[-self._current_history_size:]

            self._add_data_point()
            self._time += self.time_step

    def _add_data_point(self):
        self.data_points.append(OrderedDict({
            'time':          self._time,
            'pos':           self._position,
            'vel':           self._velocity,
            'accel':         self._acceleration,
            'voltage':       self._voltage_setpoint,
            'current':       self._current_per_motor,
            'total_current': self._current_per_motor * self.num_motors,
            'sys_voltage':   self._voltage,
            'energy':        self._energy_per_motor,
            'total_energy':  self._cumulative_energy,
            'slipping':      1 if self._slipping else 0,
            'brownout':      1 if self._brownout else 0,
            'gravity':       self._get_gravity_force()
        }))
        if self.controller is not None:
            self.data_points[-1].update(self.controller.get_data_point())

    def get_data_points(self):
        return self.data_points

    def get_final(self, key):
        return self.data_points[-1][key]

    def calc(self):
        self.update()
        self._acceleration = self._calc_max_accel(self._velocity)  # compute accel at t=0
        self._add_data_point()  # output values at t=0

        # self._integrate_with_euler()
        self._integrate_with_heun()  # numerically integrate and output using Heun's method

    def get_type(self):
        return self.__class__.__name__[:-5]

    def get_info(self):
        return ("{0}x{1}".format(self.motors.__class__.__name__,
                                 self.num_motors) if self.name is None else self.name) + \
               " @ {0}:1 - {1}m".format(round(self.gear_ratio, 3), round(self.effective_diameter, 2))

    def to_str(self):
        return "." + self.get_info() + \
               (" <{}A".format(self.motor_current_limit) if self.motor_current_limit else "") + \
               (" <{}V".format(self.motor_voltage_limit) if self.motor_voltage_limit else "")

    def to_json(self):
        output = {
            'k_resistance_s':         self.k_resistance_s,
            'k_resistance_v':         self.k_resistance_v,
            'k_gearbox_efficiency':   self.k_gearbox_efficiency,
            'gear_ratio':             self.gear_ratio,
            'effective_diameter':     self.effective_diameter,
            'compression_force':      self.compression_force,
            'incline_angle':          self.incline_angle,
            'effective_mass':         self.effective_mass,
            'check_for_slip':         self.check_for_slip,
            'coeff_kinetic_friction': self.coeff_kinetic_friction,
            'coeff_static_friction':  self.coeff_static_friction,
            'motor_current_limit':    self.motor_current_limit,
            'motor_voltage_limit':    self.motor_voltage_limit,
            'battery_voltage':        self.battery_voltage,
            'resistance_com':         self.resistance_com,
            'resistance_one':         self.resistance_one,
            'time_step':              self.time_step,
            'simulation_time':        self.simulation_time,
            'max_dist':               self.max_dist
        }
        output.update([('motor_' + k, v) for k, v in self.motors.to_json().items()])
        return output
