from optimizer import Optimizer

if __name__ == "__main__":
    elevator_config = {
        'motor_type':         '775pro',
        'num_motors':         2,

        'gear_ratio':         165,
        'effective_diameter': 2,

        'incline_angle':      90,
        'effective_mass':     550,

        'time_step':          0.001,
        'simulation_time':    100
    }
    op = Optimizer(min_ratio=100, max_ratio=300, ratio_step=5,
                   max_dist=2, distance_step=0.05,
                   model_config=elevator_config)
    op.run()
    op.save_xlsx()
