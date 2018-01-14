from controllers import PidfController
from model import ElevatorModel, plot_models
from model.motors import _775pro

if __name__ == "__main__":
    models = []

    # Elevator Gearboxes
    models += [ElevatorModel(motors=_775pro(4), gear_ratio=16, payload_mass=10,
                             pulley_diameter=2 * 0.0254, max_dist=1, motor_current_limit=30, motor_voltage_limit=12)]

    controller = PidfController()
    controller.set_deadband(0.01)
    controller.set_gains(k_p=50, k_i=0.1, k_d=0)
    controller.set_goal(1)

    models += [ElevatorModel(motors=_775pro(4), gear_ratio=16, payload_mass=10,
                             pulley_diameter=2 * 0.0254, max_dist=2, motor_current_limit=30, motor_voltage_limit=12,
                             controller=controller, simulation_time=2)]

    # # Climber Gearboxes
    # models += [ElevatorModel(motors=_775pro(4), gear_ratio=r, payload_mass=100, battery_voltage=12.3,
    #                          pulley_diameter=2 * 0.0254, max_dist=2 * 12 * 0.0254, motor_voltage_limit=12)
    #            for r in range(80, 100, 5)]

    plot_models(*models, elements_to_plot=('pos', 'vel', 'done', 'current'))
