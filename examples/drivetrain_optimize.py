from model import DrivetrainModel
from model.motors import MiniCIM, _775pro
from optimizer import Optimizer

if __name__ == "__main__":

    model = DrivetrainModel(_775pro(8), gear_ratio=26, robot_mass=68, wheel_diameter=6 * 0.0254,
                               motor_voltage_limit=12, motor_current_limit=30, max_dist=3)

    op = Optimizer(min_ratio=20, max_ratio=100, ratio_step=1,
                   max_dist=3, distance_step=0.1,
                   model=model)
    op.run()
    op.save_xlsx('/tmp/optimize_drivetrain.xlsx')
