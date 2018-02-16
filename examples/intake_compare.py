from model import IntakeShooterModel, plot_models
from model.motors import _775pro, BAG

if __name__ == "__main__":
    models = []

    # Intake Gearboxes
    models += [IntakeShooterModel(motors=BAG(2), gear_ratio=r, element_mass=3.5 / 2.2,
                                  wheel_diameter=2 * 0.0254, max_dist=7 * 0.0254, motor_voltage_limit=12,
                                  compression_force=45, check_for_slip=False) for r in [3, 4, 5, 7, 9]]
    models += [IntakeShooterModel(motors=_775pro(2), gear_ratio=r, element_mass=3.5 / 2.2,
                                  wheel_diameter=2 * 0.0254, max_dist=7 * 0.0254, motor_voltage_limit=12,
                                  compression_force=45, check_for_slip=False) for r in [3, 4, 5, 7, 9]]

    plot_models(*models, elements_to_plot=('pos', 'vel', 'total_current', 'slipping'))
