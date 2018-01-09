from math import radians

from model import ArmModel, plot_models
from model.motors import BAG

if __name__ == "__main__":

    model = ArmModel(motors=BAG(2), gear_ratio=250, arm_mass=10, arm_cg_distance=24 * 0.0254, max_dist=radians(70))
    model.calc()

    model2 = ArmModel(motors=BAG(2), gear_ratio=300, arm_mass=10, arm_cg_distance=24 * 0.0254, max_dist=radians(70))
    model2.calc()

    plot_models(model, model2, elements_to_plot=('pos', 'vel', 'current'))
