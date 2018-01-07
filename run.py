from model import DrivetrainModel

if __name__ == "__main__":
    config = {
        'motor_type':              'CIM',   # type of motor (CIM, MiniCIM, BAG, _775pro, AM_9015, AM_NeveRest, AM_RS775_125, BB_RS_775_18V, BB_RS_5)
        'num_motors':              4,       # number of motors

        'k_rolling_resistance_s':  10,      # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,       # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_drivetrain_efficiency': 0.7,     # drivetrain efficiency fraction

        'gear_ratio':              12.75,   # gear ratio
        'wheel_diameter':          6,       # wheel diameter, inches

        'vehicle_mass':            150,      # vehicle mass, lbm
        'coeff_kinetic_friction':  0.8,      # coefficient of kinetic friction
        'coeff_static_friction':   1.0,      # coefficient of static friction

        'battery_voltage':         12.7,     # fully-charged open-circuit battery volts

        'resistance_com':          0.013,    # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':          0.002,    # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':               0.001,    # integration step size, seconds
        'simulation_time':         100,      # integration duration, seconds
        'max_dist':                30        # max distance to integrate to, feet
    }

    model = DrivetrainModel.from_json(config)
    model.calc()

    config.update({
        'gear_ratio': 15,
        'max_dist': 0,
        'simulation_time': model.data_points[-1]['sim_time']
    })
    model2 = DrivetrainModel.from_json(config)
    model2.calc()

    config.update({
        'gear_ratio': 9,
        'max_dist': 0,
        'simulation_time': model.data_points[-1]['sim_time']
    })
    model3 = DrivetrainModel.from_json(config)
    model3.calc()

    model.show_plot(compare_models=[model2, model3])
