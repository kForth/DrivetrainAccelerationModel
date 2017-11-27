from model import Model

if __name__ == "__main__":
    config = {
        'motor_type':              'CIM',  # type of motor
        'num_motors':              4,  # number of motors

        'k_rolling_resistance_s':  10,  # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,  # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_drivetrain_efficiency': 0.9,  # drivetrain efficiency fraction

        'gear_ratio':              12.75,  # gear ratio
        'wheel_radius':            3,  # wheel radius, inches

        'vehicle_mass':            150,  # vehicle mass, lbm
        'coeff_kinetic_friction':  0.7,  # coefficient of kinetic friction
        'coeff_static_friction':   1.0,  # coefficient of static friction

        'battery_voltage':         12.7,  # fully-charged open-circuit battery volts

        'resistance_com':          0.013,  # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':          0.002,  # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':               0.001,  # integration step size, seconds
        'simulation_time':         1.0  # integration duration, seconds
    }

    model = Model.from_json(config)
    model.calc()
    model.print_csv()
