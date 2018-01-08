from model import ElevatorModel
from model.motors import _775pro
from optimizer import Optimizer

if __name__ == "__main__":
    model = ElevatorModel(motors=_775pro(2), gear_ratio=100, payload_mass=550, pulley_diameter=2)

    op = Optimizer(min_ratio=100, max_ratio=300, ratio_step=5,
                   max_dist=2, distance_step=0.05,
                   model=model)
    op.run()
    op.save_xlsx('/tmp/optimize_elevator.xlsx')
