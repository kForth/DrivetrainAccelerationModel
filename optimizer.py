class Optimizer:
    def __init__(self, model,
                 min_ratio=2, max_ratio=20, ratio_step=0.5,
                 min_distance=0, max_dist=40, distance_step=0.25,
                 min_time=0, max_time=10, time_step=0.001):
        self.model = model
        model.max_dist = max_dist

        self.min_distance = min_distance
        self.max_dist = max_dist
        self.distance_step = distance_step

        self.min_time = min_time
        self.max_time = max_time
        self.time_step = time_step

        self.ratios = [min_ratio]
        while self.ratios[-1] <= max_ratio:
            self.ratios += [self.ratios[-1] + ratio_step]

        self.distance_steps = [min_distance / distance_step]
        while self.distance_steps[-1] * distance_step < max_dist:
            self.distance_steps += [self.distance_steps[-1] + 1]

        self.times = [min_time]
        while self.times[-1] <= max_time:
            self.times.append(time_step * len(self.times))

        self.time_to_dist_data = []
        self.distance_at_time = []

    def run(self):
        for ratio in self.ratios:
            distance_step_deltas = [self.max_dist for _ in self.distance_steps]
            self.model.gear_ratio = ratio
            self.model.reset()
            self.model.calc()

            time_to_dist_row = [int(0)] * len(self.distance_steps)
            for point in self.model.data_points:
                dist_steps = point['pos'] / self.distance_step
                closest_index = round(dist_steps)
                dist_step_diff = abs(dist_steps - closest_index)
                if closest_index in self.distance_steps and dist_step_diff < distance_step_deltas[closest_index]:
                    distance_step_deltas[closest_index] = dist_step_diff
                    time_to_dist_row[self.distance_steps.index(closest_index)] = point['time']
            self.time_to_dist_data.append(time_to_dist_row)

            self.distance_at_time += [[e['pos'] for e in self.model.data_points]]

    def plot(self):
        import matplotlib.pyplot as plt
        import numpy as np

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        X = np.array(self.distance_steps)
        Y = np.array(self.ratios)
        X, Y = np.meshgrid(X, Y)
        Z = np.array(self.time_to_dist_data)

        ax.set_xlabel('Distance (ft)')
        ax.set_ylabel('Ratio (n:1)')
        ax.set_zlabel('Time to Dist (s)')

        surf = ax.plot_surface(X, Y, Z, cmap=plt.get_cmap('Greens'), linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()

    def save_xlsx(self, filename):
        import xlsxwriter

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.freeze_panes(2, 2)
        worksheet.set_row(0, 50)
        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, len(self.distance_steps) + 1, 5)
        top_header_format = workbook.add_format({
            'align':     'center',
            'valign':    'vcenter',
            'font_size': 28
        })
        side_header_format = workbook.add_format({
            'align':     'center',
            'valign':    'vcenter',
            'font_size': 28,
            'rotation':  90
        })
        worksheet.merge_range(0, 0, 1, 1, "Time (s)", top_header_format)
        worksheet.merge_range(0, 2, 0, len(self.distance_steps) + 1, "Distance", top_header_format)
        worksheet.merge_range(2, 0, len(self.ratios) + 1, 0, "Ratio (n:1)", side_header_format)

        for col in range(len(self.distance_steps)):
            worksheet.write(1, col + 2, self.distance_steps[col] * self.distance_step)

        for row in range(len(self.ratios)):
            worksheet.write(row + 2, 1, self.ratios[row])

        test_data = dict()
        test_data.update(self.model.to_json())
        test_data.update(self.model.motors.to_json())
        for i in range(len(self.model.to_json())):
            key = list(test_data.keys())[i]
            worksheet.write(0, len(self.distance_steps) + 2 + i, "{0}= {1}".format(key, test_data[key]))

        for col in range(len(self.distance_steps)):
            worksheet.conditional_format(2, col + 2, len(self.ratios) + 1, col + 2, {
                'type':      '3_color_scale',
                'min_color': '#00ee00',
                'mid_color': '#ffffff',
                'max_color': '#ee0000'
            })
            for row in range(len(self.ratios)):
                worksheet.write(row + 2, col + 2, self.time_to_dist_data[row][col])

        workbook.close()