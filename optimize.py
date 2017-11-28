from model import Model

import better_exceptions

if __name__ == "__main__":
    min_ratio = 2
    max_ratio = 20
    ratio_step = 0.5

    min_distance = 0
    max_distance = 40
    distance_step = 0.5

    min_time = 0
    max_time = 10
    time_step = 0.001


    config = {
        'motor_type':              'MiniCIM',  # type of motor (CIM, MiniCIM, BAG, _775pro, AM_9015, AM_NeveRest, AM_RS775_125, BB_RS_775_18V, BB_RS_5)
        'num_motors':              6,  # number of motors

        'k_rolling_resistance_s':  10,  # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,  # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_drivetrain_efficiency': 0.7,  # drivetrain efficiency fraction

        'gear_ratio':              12.75,  # gear ratio
        'wheel_diameter':          6,  # wheel diameter, inches

        'vehicle_mass':            150,  # vehicle mass, lbm
        'coeff_kinetic_friction':  0.8,  # coefficient of kinetic friction
        'coeff_static_friction':   1.0,  # coefficient of static friction

        'battery_voltage':         12.7,  # fully-charged open-circuit battery volts

        'resistance_com':          0.013,  # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':          0.002,  # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':               time_step,  # integration step size, seconds
        'simulation_time':         max_time,  # integration duration, seconds
        'max_dist':                max_distance  # max distance to integrate to, feet
    }

    ratios = [min_ratio]
    while ratios[-1] <= max_ratio:
        ratios += [ratios[-1] + ratio_step]

    distances = [min_distance]
    while distances[-1] < max_distance:
        distances += [distances[-1] + distance_step]

    times = [min_time]
    while times[-1] <= max_time:
        times.append(time_step * len(times))

    time_to_dist_data = []
    distance_at_time = []

    for ratio in ratios:
        config.update({
            'gear_ratio': ratio
        })
        model = Model.from_json(config)
        model.calc()

        time_to_dist_row = [int(0)] * len(distances)
        for point in model.data_points:
            if round(point['sim_distance']*4)/4 in distances:
                time_to_dist_row[distances.index(round(point['sim_distance']*4)/4)] = point['sim_time']
        time_to_dist_data.append(time_to_dist_row)

        distance_at_time += [[e['sim_distance'] for e in model.data_points]]

    with open('samples/optimize-time_to_dist.csv', 'w+') as file:
        file.write(",".join([""] + [str(e) for e in distances]) + "\n")
        file.write('\n'.join([','.join([str(ratios[i])] + [str(e) for e in time_to_dist_data[i]]) for i in range(len(time_to_dist_data))]))

    with open('samples/optimize-distance_at_time.csv', 'w+') as file:
        file.write(",".join([""] + [str(e) for e in times]) + "\n")
        file.write('\n'.join([','.join([str(ratios[i])] + [str(e) for e in distance_at_time[i]]) for i in range(len(distance_at_time))]))

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X = np.array(distances)
    Y = np.array(ratios)
    X, Y = np.meshgrid(X, Y)
    Z = np.array(time_to_dist_data)

    ax.set_xlabel('Distance (ft)')
    ax.set_ylabel('Ratio (n:1)')
    ax.set_zlabel('Time to Dist (s)')

    surf = ax.plot_surface(X, Y, Z, cmap=plt.get_cmap('Greens'), linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
