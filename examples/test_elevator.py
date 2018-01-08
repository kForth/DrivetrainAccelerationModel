from model import LinearModel

if __name__ == "__main__":

    config = {
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

    model = LinearModel.from_json(config)
    model.calc()

    config['gear_ratio'] = 200
    config['max_dist'] = 0
    config['simulation_time'] = model.data_points[-1]['sim_time']

    model2 = LinearModel.from_json(config)
    model2.calc()

    model.show_plot(compare_models=[model2])
