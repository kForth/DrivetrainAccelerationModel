from model import DrivetrainModel, plot_models
from model.motors import *

if __name__ == "__main__":

    model = DrivetrainModel(CIM(6), gear_ratio=12, robot_mass=150, wheel_diameter=6)
    model.calc()

    model2 = DrivetrainModel(MiniCIM(6), gear_ratio=12, robot_mass=150, wheel_diameter=6,
                             max_dist=0, simulation_time=model.get_final('time'))
    model2.calc()

    plot_models(model, model2, elements_to_plot=('pos', 'vel', 'accel'))
