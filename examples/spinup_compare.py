from model import ShooterSpinupModel, plot_models
from model.motors import _775pro

if __name__ == "__main__":
    models = []

    # Intake Gearboxes
    models += [ShooterSpinupModel(motors=_775pro(2), gear_ratio=2, wheel_inertia=1,
                                  wheel_diameter=2 * 0.0254, motor_voltage_limit=12)]
    models += [ShooterSpinupModel(motors=_775pro(2), gear_ratio=1, wheel_inertia=1,
                                  wheel_diameter=2 * 0.0254, motor_voltage_limit=12)]

    plot_models(*models, elements_to_plot=('vel', 'surface_vel', 'total_current'))
