from model import ElevatorModel
from model.motors import _775pro
from optimizer import Optimizer, RatioGenerator

if __name__ == "__main__":
    # Power Cube Elevator
    model = ElevatorModel(motors=_775pro(4), gear_ratio=15, payload_mass=10, pulley_diameter=2 * 0.0254, motor_current_limit=30)

    op = Optimizer(min_ratio=7, max_ratio=30, ratio_step=0.5,
                   max_dist=3, distance_step=0.05 * 12 * 0.0254,
                   model=model)
    #
    # # Climbing Elevator
    # model = ElevatorModel(motors=_775pro(4), gear_ratio=120, payload_mass=160, pulley_diameter=2 * 0.0254)
    #
    # op = Optimizer(model=model, min_ratio=60, max_ratio=100, ratio_step=1,
    #                max_dist=2 * 12 * 0.0254, distance_step=0.01 * 12 * 0.0254)
    op.run()
    op.save_xlsx('/tmp/optimize_elevator.xlsx')
