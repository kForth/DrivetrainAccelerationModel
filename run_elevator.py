from model.elevator import ElevatorModel

if __name__ == "__main__":
    config = {
        'motor_type':              '775pro',  # type of motor
        'num_motors':              2,         # number of motors

        'k_rolling_resistance_s':  10,        # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,         # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_gearbox_efficiency':    0.7,       # drivetrain efficiency fraction

        'gear_ratio':              80,       # gear ratio
        'pulley_diameter':         2,         # wheel diameter, inches
        'movement_angle':          90,        # movement angle in degrees relative to the ground
        'vehicle_mass':            550,       # vehicle mass, lbm

        'battery_voltage':         12.7,      # fully-charged open-circuit battery volts

        'resistance_com':          0.013,     # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':          0.002,     # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':               0.001,     # integration step size, seconds
        'simulation_time':         100,       # integration duration, seconds
        'max_dist':                1.5        # max distance to integrate to, feet
    }

    model = ElevatorModel.from_json(config)
    model.calc()

    config.update({
        'gear_ratio': 150,
        'max_dist': 0,
        'simulation_time': model.data_points[-1]['sim_time']
    })
    model2 = ElevatorModel.from_json(config)
    model2.calc()

    config.update({
        'gear_ratio': 250,
        'max_dist': 0,
        'simulation_time': model.data_points[-1]['sim_time']
    })
    model3 = ElevatorModel.from_json(config)
    model3.calc()

    model.show_plot()#compare_models=[model2, model3])
