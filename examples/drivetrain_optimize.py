from model import DrivetrainModel
from model.motors import _775pro
from optimizer import Optimizer

if __name__ == "__main__":

    model = DrivetrainModel(_775pro(8), gear_ratio=26, robot_mass=68, wheel_diameter=6 * 0.0254,
                            motor_voltage_limit=12, motor_current_limit=30, max_dist=6)

    op = Optimizer(min_ratio=10, max_ratio=50, ratio_step=1,
                   max_dist=6, distance_step=0.2,
                   model=model)
    op.run()
    op.save_xlsx('/tmp/optimize_drivetrain.xlsx')
