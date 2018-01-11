from model import DrivetrainModel, plot_models
from model.motors import _775pro, CIM

if __name__ == "__main__":
    models = []

    models += [DrivetrainModel(_775pro(8), gear_ratio=26, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=3)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=40, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=10, motor_current_limit=40, max_dist=3)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=50, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=3)]

    models += [DrivetrainModel(CIM(6), gear_ratio=10, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, max_dist=3)]

    [model.calc() for model in models]

    plot_models(*models, elements_to_plot=('pos', 'vel', 'total_current', 'current'))
