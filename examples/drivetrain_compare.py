from model import DrivetrainModel, plot_models
from model.motors import _775pro, CIM

if __name__ == "__main__":
    models = []

    # models += [DrivetrainModel(_775pro(8), gear_ratio=r, robot_mass=68, wheel_diameter=6 * 0.0254,

    # models += [DrivetrainModel(_775pro(8), gear_ratio=42, robot_mass=68, wheel_diameter=6 * 0.0254,
    #                            motor_voltage_limit=12, motor_current_limit=30, max_dist=6)]

    # models += [DrivetrainModel(_775pro(8), gear_ratio=37, robot_mass=68, wheel_diameter=6 * 0.0254,
    #                            motor_voltage_limit=12, motor_current_limit=30, max_dist=6)]
    #                            motor_voltage_limit=12, motor_current_limit=30, max_dist=3) for r in range(40, 60, 2)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=28.3, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=35, max_dist=6)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=37, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=35, max_dist=6)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=28.3, robot_mass=68, wheel_diameter=4 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=35, max_dist=6)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=20.46, robot_mass=68, wheel_diameter=4 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=35, max_dist=6)]

    models += [DrivetrainModel(CIM(6), gear_ratio=r, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, max_dist=6) for r in range(5, 12)]

    [model.calc() for model in models]

    plot_models(*models, elements_to_plot=('pos', 'vel', 'total_current'))
