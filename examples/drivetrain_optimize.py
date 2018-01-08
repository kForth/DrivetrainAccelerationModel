from model import DrivetrainModel
from model.motors import MiniCIM
from optimizer import Optimizer

if __name__ == "__main__":

    model = DrivetrainModel(MiniCIM(6), gear_ratio=12.75, wheel_diameter=6 * 0.0254, incline_angle=0, robot_mass=68)

    op = Optimizer(min_ratio=1, max_ratio=20, ratio_step=0.25,
                   max_dist=54 * 12 * 0.0254, distance_step=1 * 12 * 0.0254,
                   model=model)
    op.run()
    op.save_xlsx('/tmp/optimize_drivetrain.xlsx')
