from model import DrivetrainModel, plot_models
from model.motors import *
from model.motors import _775pro

if __name__ == "__main__":

    model = DrivetrainModel(CIM(6), gear_ratio=12, robot_mass=68, wheel_diameter=6 * 0.0254)
    model.calc()

    model2 = DrivetrainModel(MiniCIM(6), gear_ratio=12, robot_mass=68, wheel_diameter=6 * 0.0254,
                             max_dist=0, simulation_time=model.get_final('time'))
    model2.calc()

    model3 = DrivetrainModel(_775pro(8), gear_ratio=32, robot_mass=68, wheel_diameter=6 * 0.0254,
                             motor_voltage_limit=10, motor_current_limit=40,
                             max_dist=0, simulation_time=model.get_final('time'))
    model3.calc()

    plot_models(model, model2, model3, elements_to_plot=('pos', 'vel', 'accel', 'current'))
