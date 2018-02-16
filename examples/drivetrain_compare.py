from model import DrivetrainModel, ShiftingDrivetrainModel, plot_models
from model.motors import _775pro, CIM

if __name__ == "__main__":
    models = []


    # 6" Wheel Drivetrains
    models += [DrivetrainModel(_775pro(8), gear_ratio=28.3, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=10)]

    # models += [DrivetrainModel(_775pro(8), gear_ratio=28.3 * 24 / 18, robot_mass=68, wheel_diameter=6 * 0.0254,
    #                            motor_voltage_limit=12, motor_current_limit=30, max_dist=10,
    #                            name="6\" Evo Slim - w\\ external2")]

    models += [DrivetrainModel(_775pro(8), gear_ratio=28.3 * 30 / 24, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=10,
                               name="6\" Evo Slim - w\\ external")]

    models += [DrivetrainModel(_775pro(8), gear_ratio=100/12*66/16, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=10,
                               name="6\" Evo Thicc")]

    models += [ShiftingDrivetrainModel(CIM(6), robot_mass=68, max_dist=10, shift_velocity=2.3,
                                       low_gear_ratio=9,
                                       high_gear_ratio=4,
                                       wheel_diameter=4 * 0.0254,
                                       name="Oscar")]
    #
    # # # 6 CIM Drivetrain
    # models += [DrivetrainModel(CIM(6), robot_mass=68, wheel_diameter=6 * 0.0254, gear_ratio=9.07,
    #                                    motor_voltage_limit=12, max_dist=6, name="Ball Shifter 6\" Wheel")]  # Ball Shifter
    #
    # models += [DrivetrainModel(CIM(4), gear_ratio=10.75, robot_mass=68, wheel_diameter=6 * 0.0254,
    #                            motor_voltage_limit=12, max_dist=6, name="Kitbot Toughbox 6\" Wheel")]  # Kit-bot
    #
    plot_models(*models, elements_to_plot=('pos', 'vel', 'accel', 'total_current'))
