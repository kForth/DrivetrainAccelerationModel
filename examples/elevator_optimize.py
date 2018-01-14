from model import ElevatorModel
from model.motors import _775pro
from optimizer import Optimizer

if __name__ == "__main__":
    # Power Cube Elevator
    model = ElevatorModel(motors=_775pro(4), gear_ratio=16, payload_mass=10, pulley_diameter=2 * 0.0254,
                          motor_current_limit=30, motor_voltage_limit=6)

    op = Optimizer(min_ratio=7, max_ratio=30, ratio_step=0.5,
                   max_dist=3, distance_step=0.05 * 12 * 0.0254,
                   model=model)

    # # Climbing Elevator
    # model = ElevatorModel(motors=_775pro(4), gear_ratio=120, payload_mass=150, pulley_diameter=2 * 0.0254)
    #
    # op = Optimizer(model=model, min_ratio=35, max_ratio=250, ratio_step=5,
    #                max_dist=2 * 12 * 0.0254, distance_step=1 * 0.0254)
    op.run()
    op.save_xlsx('/tmp/optimize_elevator.xlsx')
