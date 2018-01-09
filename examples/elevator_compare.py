from model import ElevatorModel, plot_models
from model.motors import _775pro, CIM

if __name__ == "__main__":

    model = ElevatorModel(motors=_775pro(4), gear_ratio=165, payload_mass=250, pulley_diameter=2 * 0.0254,
                          max_dist=2 * 12 * 0.0254)

    model2 = ElevatorModel(motors=CIM(6), gear_ratio=55, payload_mass=250, pulley_diameter=2 * 0.0254,
                           max_dist=2 * 12 * 0.0254)

    model3 = ElevatorModel(motors=_775pro(8), gear_ratio=165, payload_mass=250, pulley_diameter=2 * 0.0254,
                           motor_voltage_limit=10, max_dist=2 * 12 * 0.0254)

    model.calc()
    model2.calc()
    model3.calc()

    plot_models(model, model2, model3, elements_to_plot=('pos', 'vel', 'current'))
