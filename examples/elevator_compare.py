from model import ElevatorModel, plot_models
from model.motors import _775pro

if __name__ == "__main__":
    models = []

    models += [ElevatorModel(motors=_775pro(4), gear_ratio=16, payload_mass=10,
                             pulley_diameter=2 * 0.0254, max_dist=2, motor_current_limit=30, motor_voltage_limit=6)]

    models += [ElevatorModel(motors=_775pro(4), gear_ratio=20, payload_mass=10,
                             pulley_diameter=2 * 0.0254, max_dist=2, motor_current_limit=30, motor_voltage_limit=6)]

    # models += [ElevatorModel(motors=_775pro(4), gear_ratio=r, payload_mass=160,
    #                          pulley_diameter=2 * 0.0254, max_dist=2 * 12 * 0.0254, battery_voltage=12)
    #            for r in range(80, 100, 5)]

    [model.calc() for model in models]

    plot_models(*models, elements_to_plot=('pos', 'vel', 'current'))
