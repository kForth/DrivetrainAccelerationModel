from model import ElevatorModel, plot_models
from model.motors import _775pro

if __name__ == "__main__":

    model = ElevatorModel(motors=_775pro(2), gear_ratio=165, payload_mass=550, pulley_diameter=2, max_dist=2)
    model.calc()

    model2 = ElevatorModel(motors=_775pro(2), gear_ratio=200, payload_mass=550, pulley_diameter=2,
                           max_dist=0, simulation_time=model.get_final('time'))
    model2.calc()

    plot_models(model, model2, elements_to_plot=('pos', 'vel'))
