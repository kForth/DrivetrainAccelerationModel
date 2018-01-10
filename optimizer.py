from collections import OrderedDict


class Optimizer:
    def __init__(self, model, ratio_generator=None,
                 min_ratio=2, max_ratio=20, ratio_step=0.5,
                 min_distance=0, max_dist=40, distance_step=0.25,
                 min_time=0, max_time=10, time_step=0.001):
        self.model = model
        self.ratio_generator = ratio_generator
        model.max_dist = max_dist

        self.min_distance = min_distance
        self.max_dist = max_dist
        self.distance_step = distance_step

        self.min_time = min_time
        self.max_time = max_time
        self.time_step = time_step

        if self.ratio_generator is not None:
            self.ratios = self.ratio_generator.get_ratio_list()
        else:
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

        X = np.array([i * self.distance_step for i in self.distance_steps])
        Y = np.array(self.ratios)
        Z = np.array(self.time_to_dist_data)

        X, Y = np.meshgrid(X, Y)

        ax.set_xlabel(self.model.HEADERs['pos'])
        ax.set_ylabel('Ratio (n:1)')
        ax.set_zlabel(self.model.HEADERs['time'])

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
        worksheet.merge_range(0, 0, 1, 1, self.model.HEADERS['time'], top_header_format)
        worksheet.merge_range(0, 2, 0, len(self.distance_steps) + 1, self.model.HEADERS['pos'], top_header_format)
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


class RatioGenerator:
    GEARS_32_DP = (20, 40, 60, 80, 100)
    PINIONS_32_DP = (12,)
    GEARS_20_DP = (14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 50, 62,
                   64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84)
    PINIONS_20_DP = (11, 12, 13, 14)
    SPROCKETS_25 = [16, 18, 22, 32, 34, 36, 38, 40, 42, 44, 48, 54, 58, 60, 64, 66, 72]
    SPROCKETS_35 = [12, 15, 22, 24, 26, 28, 30, 32, 33, 36, 42, 44, 48, 54, 60]
    PULLEYS_HTD_5 = (18, 24, 30, 36, 42, 60)
    PULLEYS_GT2 = (24, 36, 48, 60)
    PINION_GT2 = (12,)

    def __init__(self, gears, min_stages=1, max_stages=2, input_gears=None, min_ratio=None, max_ratio=None):
        self.gears = gears
        self.min_stages = min_stages
        self.max_stages = max_stages
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        if input_gears:
            self.input_gears = input_gears
        else:
            self.input_gears = gears

        self._ratios = {}
        self._calc()

    def _calc(self):
        gear_sets = []
        for first_stage_driving in self.input_gears:
            for first_stage_driven in self.gears:
                first_stage_ratio = first_stage_driven / first_stage_driving
                gear_sets.append({
                    'gears': [(first_stage_driving, first_stage_driven)],
                    'value': first_stage_ratio
                })

        for num_stages in range(self.min_stages + 1, self.max_stages + 1):
            for source_gear_set in list(gear_sets):
                last_driven = source_gear_set['gears'][-1][-1]
                for stage_driving in self.gears:
                    if stage_driving == last_driven:
                        continue
                    for stage_driven in self.gears:
                        if stage_driven == stage_driving:
                            continue
                        gear_set = [(stage_driving, stage_driven)]
                        if num_stages > self.min_stages + 1 and all(
                                [(source_gear_set['gears'][-1][::-1][i] == gear_set[i]) for i in range(len(gear_set))]):
                            continue
                        gear_sets.append({
                            'gears': source_gear_set['gears'] + gear_set,
                            'value': source_gear_set['value'] * (stage_driven / stage_driving)
                        })

        self._ratios = {}
        for current_set in gear_sets:
            if current_set['value'] < 1:
                key = "1:%.3f" % (1 / current_set['value'])
            else:
                key = "%.3f:1" % current_set['value']

            if key not in self._ratios.keys():
                self._ratios[key] = {
                    'ratio':            key,
                    'value': current_set['value'],
                    'gears':            [],
                }

            gear_set = (current_set['gears'][0], *sorted(current_set['gears'][1:]))
            if gear_set not in self._ratios[key]['gears']:
                self._ratios[key]['gears'].append(gear_set)
                self._ratios[key]['gears'].sort()

    def get_ratios(self):
        return OrderedDict(sorted(self._ratios.items(), key=lambda x: x[1]['value']))

    def get_ratio_list(self):
        ratios = [e['value'] for e in self._ratios.values()]
        max_ratio = self.max_ratio if self.max_ratio is not None else max(ratios)
        min_ratio = self.min_ratio if self.min_ratio is not None else min(ratios)
        return sorted([e for e in ratios if max_ratio >= e >= min_ratio])
