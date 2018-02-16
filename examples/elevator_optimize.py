from model import ElevatorModel
from model.motors import _775pro, CIM, MiniCIM
from optimizer import Optimizer

if __name__ == "__main__":
    # Power Cube Elevator
    # model = ElevatorModel(motors=CIM(2), gear_ratio=16, payload_mass=10, pulley_diameter=2.144 * 0.0254,
    #                       motor_current_limit=40)
    #
    # op = Optimizer(min_ratio=7, max_ratio=30, ratio_step=0.5,
    #                max_dist=3, distance_step=0.05 * 12 * 0.0254,
    #                model=model)

    # # Climbing Elevator
    model = ElevatorModel(motors=MiniCIM(3), gear_ratio=26, payload_mass=300/2.2, battery_voltage=12.3,
                         pulley_diameter=1.43 * 0.0254, max_dist=32*0.0254, motor_voltage_limit=12)

    op = Optimizer(model=model, min_ratio=12, max_ratio=40, ratio_step=1,
                   max_dist=32 * 0.0254, distance_step=2 * 0.0254)
    op.run()
    op.save_xlsx('/tmp/optimize_elevator.xlsx')
