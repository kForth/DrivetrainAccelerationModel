from model import Model

if __name__ == "__main__":
    config = {
        'motor_type': 'CIM',
        'num_motors': 4,

        'k_rolling_resistance_s': 10,
        'k_rolling_resistance_v': 0,
        'k_drivetrain_efficiency': 0.9,

        'gear_ratio': 12.75,
        'wheel_radius': 3,

        'vehicle_mass': 150,
        'coeff_kinetic_friction': 0.7,
        'coeff_static_friction': 1.0,

        'battery_voltage': 12.7,

        'resistance_com': 0.013,
        'resistance_one': 0.002,

        'time_step': 0.001,
        'simulation_time': 1.0
    }

    model = Model.from_json(config)
    model.calc()
    model.print_csv()
