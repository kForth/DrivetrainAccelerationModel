from model import DrivetrainModel, ShiftingDrivetrainModel, plot_models
from model.motors import _775pro

if __name__ == "__main__":
    models = []

    # 5" Wheel Drivetrains
    models += [DrivetrainModel(_775pro(8), gear_ratio=28.3, robot_mass=68, wheel_diameter=5 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=6)]

    models += [ShiftingDrivetrainModel(_775pro(8), robot_mass=68, max_dist=6, shift_velocity=2.6,  # 2.15, 2.7
                                       low_gear_ratio=(85 / 12 * 52 / 18 * 50 / 25),
                                       high_gear_ratio=(85 / 12 * 46 / 24 * 50 / 25),
                                       wheel_diameter=5 * 0.0254, motor_voltage_limit=12,
                                       low_gear_current_limit=25, high_gear_current_limit=15)]

    # 6" Wheel Drivetrains
    # models += [DrivetrainModel(_775pro(8), gear_ratio=28.3, robot_mass=68, wheel_diameter=6 * 0.0254,
    #                            motor_voltage_limit=12, motor_current_limit=30, max_dist=6)]

    models += [DrivetrainModel(_775pro(8), gear_ratio=28.3 * 30 / 24, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=6)]

    models += [ShiftingDrivetrainModel(_775pro(8), robot_mass=68, max_dist=6, shift_velocity=2.8,  # 2.85, 2.55
                                       low_gear_ratio=(85 / 12 * 56 / 14 * 46 / 29),
                                       high_gear_ratio=(85 / 12 * 52 / 18 * 46 / 29),
                                       wheel_diameter=6 * 0.0254, motor_voltage_limit=12,
                                       low_gear_current_limit=25, high_gear_current_limit=15)]

    # # 6 CIM Drivetrain
    # models += [DrivetrainModel(CIM(6), gear_ratio=9, robot_mass=68, wheel_diameter=6 * 0.0254,
    #                            motor_voltage_limit=12, motor_current_limit=50, max_dist=6)]

    [model.calc() for model in models]

    plot_models(*models, elements_to_plot=('pos', 'vel', 'total_energy'))
