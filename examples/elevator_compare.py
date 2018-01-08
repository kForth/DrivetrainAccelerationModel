from model import ElevatorModel
from model.util import plot_models

if __name__ == "__main__":

    model = ElevatorModel(motor_type='775pro', num_motors=2, gear_ratio=165, payload_mass=550, pulley_diameter=2,
                          max_dist=2)
    model.calc()

    model2 = ElevatorModel(motor_type='775pro', num_motors=2, gear_ratio=200, payload_mass=550, pulley_diameter=2,
                           max_dist=0, simulation_time=model.get_final('time'))
    model2.calc()

    plot_models(model, model2, elements_to_plot=('pos', 'vel'))
