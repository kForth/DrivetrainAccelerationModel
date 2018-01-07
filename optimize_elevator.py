from model import ElevatorModel

import better_exceptions

if __name__ == "__main__":
    save_csv = False
    plot = False
    save_xlsx = True

    min_ratio = 100
    max_ratio = 300
    ratio_step = 5

    min_distance = 0
    max_distance = 2
    distance_step = 0.05

    min_time = 0
    max_time = 100
    time_step = 0.001

    config = {
        'motor_type':              '775pro',  # type of motor
        'num_motors':              2,         # number of motors

        'k_rolling_resistance_s':  10,        # rolling resistance tuning parameter, lbf
        'k_rolling_resistance_v':  0,         # rolling resistance tuning parameter, lbf/(ft/sec)
        'k_gearbox_efficiency':    0.7,       # drivetrain efficiency fraction

        'gear_ratio':              250,       # gear ratio
        'pulley_diameter':         2,         # wheel diameter, inches
        'movement_angle':          90,        # movement angle in degrees relative to the ground
        'vehicle_mass':            550,       # vehicle mass, lbm

        'battery_voltage':         12.7,      # fully-charged open-circuit battery volts

        'resistance_com':          0.013,     # battery and circuit resistance from bat to PDB (incl main breaker), ohms
        'resistance_one':          0.002,     # circuit resistance from PDB to motor (incl 40A breaker), ohms

        'time_step':       time_step,  # integration step size, seconds
        'simulation_time': max_time,  # integration duration, seconds
        'max_dist':        max_distance  # max distance to integrate to, feet
    }

    ratios = [min_ratio]
    while ratios[-1] <= max_ratio:
        ratios += [ratios[-1] + ratio_step]

    distances = [min_distance / distance_step]
    while distances[-1] * distance_step < max_distance:
        distances += [(distances[-1] + 1)]

    times = [min_time]
    while times[-1] <= max_time:
        times.append(time_step * len(times))

    time_to_dist_data = []
    distance_at_time = []
    models = []

    for ratio in ratios:
        config.update({
            'gear_ratio': ratio
        })
        model = ElevatorModel.from_json(config)
        model.calc()
        models.append(model)

        time_to_dist_row = [int(0)] * len(distances)
        for point in model.data_points:
            index = round(point['sim_distance'] / distance_step)
            print(index)
            if index in distances:
                time_to_dist_row[distances.index(index)] = point['sim_time']
        time_to_dist_data.append(time_to_dist_row)

        distance_at_time += [[e['sim_distance'] for e in model.data_points]]

    if save_csv:
        with open('samples/optimize-time_to_dist.csv', 'w+') as file:
            file.write(",".join([""] + [str(e) for e in distances]) + "\n")
            file.write('\n'.join([','.join([str(ratios[i])] + [str(e) for e in time_to_dist_data[i]]) for i in range(len(time_to_dist_data))]))

        with open('samples/optimize-distance_at_time.csv', 'w+') as file:
            file.write(",".join([""] + [str(e) for e in times]) + "\n")
            file.write('\n'.join([','.join([str(ratios[i])] + [str(e) for e in distance_at_time[i]]) for i in range(len(distance_at_time))]))

    if plot:
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

    if save_xlsx:
        import xlsxwriter

        workbook = xlsxwriter.Workbook('samples/optimize.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.freeze_panes(2, 2)
        worksheet.set_row(0, 50)
        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, len(distances) + 1, 5)
        top_header_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 28
        })
        side_header_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 28,
            'rotation': 90
        })
        worksheet.merge_range(0, 0, 1, 1, "Time (s)", top_header_format)
        worksheet.merge_range(0, 2, 0, len(distances) + 1, "Distance (ft)", top_header_format)
        worksheet.merge_range(2, 0, len(ratios) + 1, 0, "Ratio (n:1)", side_header_format)

        for col in range(len(distances)):
            worksheet.write(1, col+2, distances[col] * distance_step)

        for row in range(len(ratios)):
            worksheet.write(row+2, 1, ratios[row])

        test_data = {}
        model = models[0]
        test_data.update(model.to_json())
        test_data.update(model.motor.to_json())
        for i in range(len(model.to_json())):
            key = list(test_data.keys())[i]
            worksheet.write(0, len(distances) + 2 + i, "{0}= {1}".format(key, test_data[key]))

        for col in range(len(distances)):
            worksheet.conditional_format(2, col + 2, len(ratios) + 1, col + 2, {
                'type': '3_color_scale',
                'min_color': '#00ee00',
                'mid_color': '#ffffff',
                'max_color': '#ee0000'
            })
            for row in range(len(ratios)):
                worksheet.write(row + 2, col + 2, time_to_dist_data[row][col])

        workbook.close()
