import colorsys
from random import randint

import matplotlib.pyplot as plt
from matplotlib import lines, patches

from model._arm import ArmModel
from model._custom import CustomModel
from model._drivetrain import DrivetrainModel
from model._elevator import ElevatorModel


def plot_models(*models, elements_to_plot=('pos', 'vel', 'accel')):
    fig, ax = plt.subplots()

    line_types = [[100000, 1], [3, 1]]

    line_colours = []
    for i in range(len(models)):
        hue = (i / (len(models)))
        luminance = 0.5 + randint(0, 10)/100
        saturation = 0.5 + randint(0, 10)/100

        line_colours.append(colorsys.hls_to_rgb(hue, luminance, saturation))

    for i in range(2, len(elements_to_plot)):
        line_types += [line_types[-1] + [1, 1]]

    ax.set(xlabel='time (s)', title='{} Acceleration Model'.format(models[0].get_type()))
    ax.grid()
    for i in range(min(len(models), len(line_colours))):
        model = models[i]
        t = [e['time'] for e in model.data_points]

        for j in range(len(elements_to_plot)):
            key = elements_to_plot[j]
            ax.plot(t, [(e[key] / model.PLOT_FACTORS[key]) for e in model.data_points], label=key,
                    color=line_colours[i], dashes=line_types[j])

    handles = []
    handles += [patches.Patch(color=line_colours[i],
                              label=models[i].to_str())
                for i in range(min(len(models), len(line_colours)))]
    headers = models[0].HEADERS
    for i in range(len(elements_to_plot)):
        label = headers[elements_to_plot[i]] if elements_to_plot[i] in headers else elements_to_plot[i]
        handles += [lines.Line2D([], [], color='k', dashes=line_types[i], label=label)]
    plt.legend(handles=handles)

    plt.show()


def dump_model_csv(model, filename):
    data_points = model.get_data_points()
    headers = list(model.get_data_points()[0].keys()) + \
              [(e + "=" + str(model.to_json()[e])) for e in list(model.to_json().keys())]

    csv_lines = [list(e.values()) for e in data_points]
    csv_lines = [[str(format(e, '.5f') if isinstance(e, float) else e) for e in line] for line in csv_lines]
    csv_str = "\n".join(headers + [",".join(e) for e in csv_lines])

    open(filename, "w+").write(csv_str)
