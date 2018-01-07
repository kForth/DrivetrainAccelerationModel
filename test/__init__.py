from model import DrivetrainModel


def test_load_from_json():
    config = dict(DrivetrainModel.SAMPLE_CONFIG)
    model = DrivetrainModel.from_json(config)
    config['k_rolling_resistance_s'] *= 4.448222  # convert lbf to Newtons
    config['k_rolling_resistance_v'] *= 4.448222 * 3.28083  # convert lbf/(ft/s) to Newtons/(meter/sec)
    config['wheel_diameter'] = config['wheel_diameter']  # convert inches to meters
    config['vehicle_mass'] *= 0.4535924  # convert lbm to kg

    bad_keys = []
    for key in config.keys():
        if model.__dict__[key] != config[key]:
            bad_keys += [key]
    return (False, bad_keys) if bad_keys else True


def test_output1():
    from os import path
    output1 = open(path.dirname(__file__) + '/output1.txt').read()
    config =  {
        'motor_type':              'CIM',  # type of motor
        'num_motors':              4,  # number of motors

        'k_rolling_resistance_s':  10,  # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,  # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_drivetrain_efficiency': 0.7,  # drivetrain efficiency fraction

        'gear_ratio':              12.75,  # gear ratio
        'wheel_diameter':          6,  # wheel radius, inches

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
    model = DrivetrainModel.from_json(config)
    model.calc()
    return model.get_csv_str() == output1


if __name__ == "__main__":
    for test in [test_load_from_json, test_output1]:
        print(test, test())
