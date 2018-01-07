from model import LinearModel

if __name__ == "__main__":
    drivetrain_config = {
        'motor_type':             'CIM',
        'num_motors':             4,
        # 'motor_current_limit':    60,

        'gear_ratio':             12.75,
        'effective_diameter':     6,

        'incline_angle':          0,
        'effective_mass':         150,

        'check_for_slip':         True,
        'coeff_kinetic_friction': 0.8,
        'coeff_static_friction':  1.0,

        'simulation_time':        100,
        'max_dist':               30,

        'elements_to_plot':       (0, 1, 2, 3)
    }

    elevator_config = {
        'motor_type':         '775pro',  # type of motor
        'num_motors':         2,  # number of motors
        # 'motor_current_limit':     40,

        'gear_ratio':         165,  # gear ratio
        'effective_diameter': 2,  # effective diameter, inches

        'incline_angle':      90,  # incline angle relative to the ground, degrees
        'effective_mass':     550,  # effective mass, lbm

        'simulation_time':    30,  # integration duration, seconds
        'max_dist':           2,  # max distance to integrate to, feet

        'elements_to_plot':   [0, 1, 3]  # plot pos, vel, current/10
    }

    # config = elevator_config
    config = drivetrain_config

    model = LinearModel.from_json(config)
    model.calc()

    config['gear_ratio'] -= config['gear_ratio'] * 0.2
    config['max_dist'] = 0
    config['simulation_time'] = model.data_points[-1]['sim_time']

    model2 = LinearModel.from_json(config)
    model2.calc()

    config['gear_ratio'] += config['gear_ratio'] * 0.4

    model3 = LinearModel.from_json(config)
    model3.calc()

    model.show_plot(compare_models=[model2, model3])
