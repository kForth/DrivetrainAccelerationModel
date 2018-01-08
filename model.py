from collections import OrderedDict
from math import pi, radians, sin

from matplotlib import lines, patches

from motors import MOTOR_LOOKUP


class LinearModel:
    SAMPLE_CONFIG = {
        'motor_type':             'CIM',  # type of motor
        'num_motors':             4,  # number of motors

        'k_resistance_s': 10,  # rolling resistance tuning parameter, lbf
        'k_resistance_v': 0,  # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_gearbox_efficiency':   0.7,  # gearbox efficiency fraction

        'gear_ratio':             12.75,  # gear ratio
        'effective_diameter':     6,  # wheel radius, inches
        'incline_angle':          0,  # incline angle relative to the ground, degrees
        'effective_mass':         150,  # effective mass, lbm

        'check_for_slip':         False,  # flag if we should account of wheel slip in drivetrains
        'coeff_kinetic_friction': 0.8,  # coefficient of kinetic friction
        'coeff_static_friction':  1.0,  # coefficient of static friction

        'motor_current_limit':    1000,  # current limit per motor

        'battery_voltage':        12.7,  # fully-charged open-circuit battery volts

        'resistance_com':         0.013,  # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':         0.002,  # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':              0.001,  # integration step size, seconds
        'simulation_time':        100,  # integration duration, seconds
        'max_dist':               30,  # max distance to integrate to, feet

        'elements_to_plot':                   (0, 1, 2)  # elements to plot (pos, vel, accel, current)
    }

    csv_headers = ['time(s)', 'dist(ft)', 'speed(ft/s)', 'accel(ft/s^2)', 'current(amps/10)', 'voltage', 'slip']
    line_colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    line_types = ['-', '--', '-.', ':']

    def __init__(self, motor_type, num_motors, k_resistance_s, k_resistance_v, k_gearbox_efficiency,
                 gear_ratio, effective_diameter, effective_mass, check_for_slip, coeff_kinetic_friction, coeff_static_friction,
                 battery_voltage, resistance_com, resistance_one, time_step, simulation_time, max_dist,
                 incline_angle, elements_to_plot, motor_current_limit):
        self.motor_type = motor_type
        self.motor = MOTOR_LOOKUP[motor_type.lower().replace(' ', '').replace('_', '')](num_motors)
        self.num_motors = num_motors
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
        self.elements_to_plot = elements_to_plot
        self.config_backup = dict([(e, self.__dict__[e]) for e in LinearModel.SAMPLE_CONFIG.keys()])

        # calculate Derived Constants
        self._convert_units_to_si()

        self.effective_weight = self.effective_mass * 9.80665  # effective weight, Newtons

        self.is_slipping = False  # state variable, init to false
        self.sim_time = 0  # elapsed time, seconds
        self.sim_distance = 0  # distance traveled, meters
        self.sim_speed = 0  # speed, meters/sec
        self.sim_acceleration = 0  # acceleration, meters/sec/sec
        self.sim_voltage = 0  # Voltage at the motor
        self.sim_current_per_motor = 0  # current per motor, amps

        self.csv_lines = []
        self.data_points = []

    def reset(self):
        self.is_slipping = False  # state variable, init to false
        self.sim_time = 0  # elapsed time, seconds
        self.sim_distance = 0  # distance traveled, meters
        self.sim_speed = 0  # speed, meters/sec
        self.sim_acceleration = 0  # acceleration, meters/sec/sec
        self.sim_voltage = 0  # Voltage at the motor
        self.sim_current_per_motor = 0  # current per motor, amps

        self.csv_lines = []
        self.data_points = []

    def _convert_units_to_si(self):
        self.k_resistance_s *= 4.448222  # convert lbf to Newtons
        self.k_resistance_v *= 4.448222 * pi * 2  # convert lbf/(ft/s) to Newtons/(meter/sec)
        self.effective_radius = self.effective_radius * 2.54 / 100  # convert inches to meters
        self.effective_mass *= 0.4535924  # convert lbm to kg

    def _calc_max_accel(self, velocity):  # compute acceleration w/ slip
        motor_speed = velocity / self.effective_radius * self.gear_ratio  # motor speed associated with pulley speed

        self.sim_current_per_motor = (self.sim_voltage - (motor_speed / self.motor.k_v)) / self.motor.k_r
        if velocity > 0:
            self.sim_current_per_motor = min(self.sim_current_per_motor, self.motor_current_limit)
        max_torque_at_voltage = self.motor.k_t * self.sim_current_per_motor

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
        force_from_gravity = self.effective_weight * sin(radians(self.incline_angle))
        net_accel_force = applied_force_at_wheel - rolling_resistance - force_from_gravity  # net force available, in newtons
        if net_accel_force < 0:
            net_accel_force = 0
        return net_accel_force / self.effective_mass

    def _integrate_with_heun(self):  # numerical integration using Heun's Method
        self.sim_time = self.time_step
        while self.sim_time < self.simulation_time + self.time_step and \
                (self.sim_distance * pi * 2 < self.max_dist or self.max_dist <= 0):
            v_temp = self.sim_speed + self.sim_acceleration * self.time_step  # kickstart with Euler step
            a_temp = self._calc_max_accel(v_temp)
            v_temp = self.sim_speed + (self.sim_acceleration + a_temp) / 2 * \
                                      self.time_step  # recalc v_temp trapezoidally
            self.sim_acceleration = self._calc_max_accel(v_temp)  # update a
            self.sim_distance += (self.sim_speed + v_temp) / 2 * self.time_step  # update x trapezoidally
            self.sim_speed = v_temp  # update V
            self._add_data_point()
            self.sim_time += self.time_step

    def _add_data_point(self):
        self.data_points.append(OrderedDict({
            'sim_time':          self.sim_time,
            'sim_distance':      self.sim_distance * pi * 2,
            'sim_speed':         self.sim_speed * pi * 2,
            'sim_acceleration ': self.sim_acceleration * pi * 2,
            'sim_current':       self.sim_current_per_motor / 10,
            'sim_voltage':       self.sim_voltage,
            'is_slipping':       self.is_slipping
        }))
        self.csv_lines.append(list(self.data_points[-1].values()))

    def calc(self):
        self.csv_lines.append(self.csv_headers +
                              [e + "=" + str(self.config_backup[e]) for e in self.config_backup.keys()] +
                              [e + "=" + str(self.motor.to_json()[e]) for e in self.motor.to_json()])

        self.sim_acceleration = self._calc_max_accel(self.sim_speed)  # compute accel at t=0
        self._add_data_point()  # output values at t=0

        self._integrate_with_heun()  # numerically integrate and output using Heun's method

    def get_csv_str(self):
        return "\n".join([",".join([str(format(e, '.5f') if isinstance(e, float) else e) for e in line])
                          for line in self.csv_lines])

    def print_csv(self):
        print(self.get_csv_str())

    def save_csv(self, filename):
        open(filename, "w+").write(self.get_csv_str())

    def plot_data(self, ax, csv_lines, i=0):
        t = [e[0] for e in csv_lines[1:]]
        for j in range(len(self.line_types)):
            if j not in self.elements_to_plot:
                continue
            line = self.line_colours[i % len(self.line_colours)] + self.line_types[j]
            ax.plot(t, [e[j + 1] for e in csv_lines[1:]], line, label=self.csv_headers[j + 1])

    def show_plot(self, compare_models=[]):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        if not isinstance(compare_models, list):
            compare_models = [compare_models]

        ax.set(xlabel='time (s)', title='Drivetrain Acceleration Model')
        ax.grid()

        models = [self] + compare_models
        for i in range(len(models)):
            model = models[i]
            self.plot_data(ax, model.csv_lines, i)
        handles = []
        handles += [patches.Patch(color=self.line_colours[i],
                                  label='{0}x {1} @ {2}:1 - {3}in'.format(
                                          str(models[i].num_motors),
                                          models[i].motor_type,
                                          models[i].gear_ratio,
                                          models[i].effective_diameter))
                    for i in range(len(models))]
        handles += [lines.Line2D([], [], color='k', linestyle=self.line_types[i],
                                 label=self.csv_headers[i + 1]) for i in range(len(self.line_types)) if i in self.elements_to_plot]
        plt.legend(handles=handles)

        plt.show()

    def to_json(self):
        return self.config_backup

    @staticmethod
    def from_json(data):
        # if all([k in LinearModel.SAMPLE_CONFIG.keys() for k in data.keys()]):
        temp = LinearModel.SAMPLE_CONFIG
        temp.update(data)
        return LinearModel(**temp)
