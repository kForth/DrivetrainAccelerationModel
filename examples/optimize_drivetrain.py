from optimizer import Optimizer

if __name__ == "__main__":
    drivetrain_config = {
        'motor_type':             'MiniCIM',
        'num_motors':             6,

        'gear_ratio':             12.75,
        'effective_diameter':     6,

        'incline_angle':          0,
        'effective_mass':         150,

        'check_for_slip':         True,
        'coeff_kinetic_friction': 0.8,
        'coeff_static_friction':  1.0
    }

    op = Optimizer(min_ratio=1, max_ratio=20, ratio_step=0.25,
                   max_dist=54, distance_step=1,
                   model_config=drivetrain_config)
    op.run()
    op.save_xlsx(filename='../samples/optimize.xlsx')
