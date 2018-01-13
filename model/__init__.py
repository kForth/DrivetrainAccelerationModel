import colorsys
from random import randint

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import lines, patches

from model._arm import ArmModel
from model._custom import CustomModel
from model._drivetrain import DrivetrainModel
from model._shifting_drivetrain import ShiftingDrivetrainModel
from model._elevator import ElevatorModel


def plot_models(*models, elements_to_plot=('pos', 'vel', 'accel')):
    fig, ax = plt.subplots()

    line_colours = []
    for i in range(len(models)):
        hue = (i / (len(models)))
        luminance = 0.5 + randint(0, 10) / 100
        saturation = 0.5 + randint(0, 10) / 100

        line_colours.append(colorsys.hls_to_rgb(hue, luminance, saturation))

    line_types = [[100000, 1], [3, 1]]
    for i in range(2, len(elements_to_plot)):
        line_types += [line_types[-1] + [1, 1]]

    ax.set_yticks(np.arange(0, 1000, 1))
    # ax.set_yticks(np.arange(0, 101, 1), minor=True)
    ax.set_xticks(np.arange(0, 100, 0.5))
    ax.set_xticks(np.arange(0, 100, 0.1), minor=True)

    ax.set(xlabel='time (s)', title='{} Acceleration Model'.format(models[0].get_type()))
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    legend_handles = []
    handle_lines = []
    for i in range(len(models)):
        model = models[i]
        t = [e['time'] for e in model.data_points]
        model_lines = []
        for j in range(len(elements_to_plot)):
            key = elements_to_plot[j]
            model_lines += ax.plot(t, [(e[key] / model.PLOT_FACTORS[key]) for e in model.data_points], label=key,
                                    color=line_colours[i], dashes=line_types[j])
        handle_lines.append(model_lines)
        handle = patches.Patch(color=line_colours[i], label=models[i].to_str())
        legend_handles.append(handle)

    headers = models[0].HEADERS
    model_lines = list(handle_lines)
    for i in range(len(elements_to_plot)):
        label = headers[elements_to_plot[i]] if elements_to_plot[i] in headers else elements_to_plot[i]
        handle = lines.Line2D([], [], color='k', dashes=line_types[i], label=label)
        handle_lines.append([e[i] for e in model_lines])
        legend_handles.append(handle)
    legend = ax.legend(handles=legend_handles, fancybox=True)

    line_handle_dict = dict()
    handle_visibility = dict()
    line_visibility = dict()
    for handle, model_lines in zip(legend.legendHandles, handle_lines):
        handle.set_picker(5)  # 5 pts tolerance
        line_handle_dict[handle] = model_lines
        handle_visibility[handle] = True
        for line in model_lines:
            if line in line_visibility.keys():
                continue
            line_visibility[line] = 1

    def handle_pick_event(event):
        handle = event.artist
        handle_lines = line_handle_dict[handle]
        should_be_visible = not handle_visibility[handle]
        for line in handle_lines:
            line_visibility[line] += 1 if should_be_visible else -1
            line.set_visible(line_visibility[line] > 0)
        if legend.legendHandles.index(handle) < len(models):
            handle.set_color(list(line_colours[legend.legendHandles.index(handle)]) + [1.0 if should_be_visible else 0.2])
        else:
            handle.set_color([0, 0, 0, 1.0 if should_be_visible else 0.2])
        handle_visibility[handle] = should_be_visible
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', handle_pick_event)
    plt.show()


def dump_model_csv(model, filename):
    data_points = model.get_data_points()
    headers = list(model.get_data_points()[0].keys()) + \
              [(e + "=" + str(model.to_json()[e])) for e in list(model.to_json().keys())]

    csv_lines = [list(e.values()) for e in data_points]
    csv_lines = [[str(format(e, '.5f') if isinstance(e, float) else e) for e in line] for line in csv_lines]
    csv_str = "\n".join(headers + [",".join(e) for e in csv_lines])

    open(filename, "w+").write(csv_str)
