from model.generic import GenericModel


class ElevatorModel(GenericModel):
    def __init__(self,
                 motor_type: str,
                 num_motors: int,
                 gear_ratio: float,
                 pulley_diameter: float,
                 payload_mass: float,
                 incline_angle=90,
                 motor_current_limit=None,
                 k_gearbox_efficiency=0.7,
                 coeff_kinetic_friction=0.8,
                 coeff_static_friction=1.0,
                 k_resistance_s=0,
                 k_resistance_v=0,
                 battery_voltage=12.5,
                 resistance_com=0.013,
                 resistance_one=0.002,
                 max_dist=50,
                 time_step=0.001,
                 simulation_time=120.0):

        super().__init__(motor_type, num_motors, k_resistance_s, k_resistance_v, k_gearbox_efficiency, gear_ratio,
                         pulley_diameter, payload_mass, True, coeff_kinetic_friction, coeff_static_friction,
                         battery_voltage, resistance_com, resistance_one, time_step, simulation_time, max_dist,
                         incline_angle, motor_current_limit)
