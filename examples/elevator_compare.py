from pprint import pprint

from model import ElevatorModel, plot_models
from model.motors import _775pro
from optimizer import RatioGenerator

if __name__ == "__main__":
    models = []

    # models += [ElevatorModel(motors=_775pro(4), gear_ratio=60 / 12 * 60 / 20, payload_mass=10,
    #                          pulley_diameter=2 * 0.0254, max_dist=2, motor_current_limit=30)]

    ratio_generator = RatioGenerator(RatioGenerator.GEARS_32_DP, input_gears=(12,),
                                     max_stages=3, min_ratio=60, max_ratio=100)

    models += [ElevatorModel(motors=_775pro(4), gear_ratio=r, payload_mass=160,
                             pulley_diameter=2 * 0.0254, max_dist=2 * 12 * 0.0254, battery_voltage=12)
               for r in ratio_generator.get_ratio_list()]

    [model.calc() for model in models]

    print(len(ratio_generator.get_ratios()))

    # plot_models(*models, elements_to_plot=('pos', 'vel', 'current', 'voltage', 'total_energy'))
