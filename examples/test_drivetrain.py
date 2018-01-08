from model.drivetrain import DrivetrainModel
from model.util import plot_models

if __name__ == "__main__":

    model = DrivetrainModel(motor_type='CIM', num_motors=6, gear_ratio=12, robot_mass=150, wheel_diameter=6).calc()

    model2 = DrivetrainModel(motor_type='MiniCIM', num_motors=6, gear_ratio=12, robot_mass=150, wheel_diameter=6,
                             max_dist=0, simulation_time=model.get_final('time')).calc()

    plot_models(model, model2, elements_to_plot=('pos', 'vel', 'accel'))
