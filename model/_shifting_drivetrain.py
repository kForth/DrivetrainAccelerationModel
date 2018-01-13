from model._custom import CustomModel
from model.motors import Motor


class ShiftingDrivetrainModel(CustomModel):
    def __init__(self,
                 motors: Motor,
                 low_gear_ratio: float,
                 high_gear_ratio: float,
                 wheel_diameter: float,
                 robot_mass: float,
                 shift_velocity: float,
                 incline_angle=0,
                 low_gear_current_limit=None,
                 high_gear_current_limit=None,
                 motor_peak_current_limit=None,
                 motor_voltage_limit=None,
                 k_gearbox_efficiency=0.7,
                 coeff_kinetic_friction=0.8,
                 coeff_static_friction=1.0,
                 k_resistance_s=0,
                 k_resistance_v=0,
                 battery_voltage=12.5,
                 resistance_com=0.013,
                 resistance_one=0.002,
                 time_step=0.001,
                 simulation_time=120.0,
                 max_dist=8,
                 initial_position=0,
                 initial_velocity=0,
                 initial_acceleration=0):

        super().__init__(motors=motors,
                         k_resistance_s=k_resistance_s,
                         k_resistance_v=k_resistance_v,
                         k_gearbox_efficiency=k_gearbox_efficiency,
                         gear_ratio=low_gear_ratio,
                         effective_diameter=wheel_diameter,
                         effective_mass=robot_mass,
                         check_for_slip=True,
                         coeff_kinetic_friction=coeff_kinetic_friction,
                         coeff_static_friction=coeff_static_friction,
                         battery_voltage=battery_voltage,
                         resistance_com=resistance_com,
                         resistance_one=resistance_one,
                         time_step=time_step,
                         simulation_time=simulation_time,
                         max_dist=max_dist,
                         incline_angle=incline_angle,
                         motor_current_limit=low_gear_ratio,
                         motor_peak_current_limit=motor_peak_current_limit,
                         motor_voltage_limit=motor_voltage_limit,
                         initial_position=initial_position,
                         initial_velocity=initial_velocity,
                         initial_acceleration=initial_acceleration)
        self.high_gear_current_limit = high_gear_current_limit
        self.low_gear_current_limit = low_gear_current_limit
        self.shift_velocity = shift_velocity
        self.high_gear_ratio = high_gear_ratio
        self.low_gear_ratio = low_gear_ratio

    def get_info(self):
        return "{0}x{1} @ ({2}/{3}):1 - {4}m".format(self.motors.__class__.__name__, self.num_motors,
                                                     round(self.low_gear_ratio, 3), round(self.high_gear_ratio, 3),
                                                     round(self.effective_diameter, 2))

    def to_str(self):
        return "." + self.get_info() + \
               (" <({0}/{1})A".format(self.low_gear_current_limit, self.high_gear_current_limit)
                if self.low_gear_current_limit or self.high_gear_current_limit else "") + \
               (" <{}V".format(self.motor_voltage_limit) if self.motor_voltage_limit else "")

    def control_update(self):
        if self._velocity > self.shift_velocity:
            if self.gear_ratio is not self.high_gear_ratio:
                self._was_current_limited = False
            self.motor_current_limit = self.high_gear_current_limit
            self.gear_ratio = self.high_gear_ratio
        else:
            self.motor_current_limit = self.low_gear_current_limit
            self.gear_ratio = self.low_gear_ratio
