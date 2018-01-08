from model import Model
from model.util import plot_models

if __name__ == "__main__":

    config = {
        'motor_type':         '775pro',
        'num_motors':         2,

        'gear_ratio':         165,
        'effective_diameter': 2,

        'incline_angle':      90,
        'effective_mass':     550,

        'simulation_time':    30,
        'max_dist':           2
    }

    model = Model.from_json(config)
    model.calc()

    config['gear_ratio'] = 200
    config['max_dist'] = 0
    config['simulation_time'] = model.data_points[-1]['time']

    model2 = Model.from_json(config)
    model2.calc()

    plot_models(model, model2, elements_to_plot=('pos', 'vel', 'current'))
