from model import Model
from model.util import plot_models, dump_model_csv

if __name__ == "__main__":

    config = {
        'motor_type':             'CIM',
        'num_motors':             6,

        'gear_ratio':             13,
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

    model = Model.from_json(config)
    model.calc()

    config['motor_type'] = 'MiniCIM'
    config['max_dist'] = 0
    config['simulation_time'] = model.data_points[-1]['sim_time']

    model2 = Model.from_json(config)
    model2.calc()

    plot_models(model, model2)
