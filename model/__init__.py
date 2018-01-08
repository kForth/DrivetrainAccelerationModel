import matplotlib.pyplot as plt
from matplotlib import lines, patches

from model.drivetrain import DrivetrainModel
from model.elevator import ElevatorModel
from model.generic import GenericModel


def plot_models(*models, elements_to_plot=('pos', 'vel', 'accel')):
    fig, ax = plt.subplots()

    line_colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    line_types = ['-', '--', '-.', ':']

    headers = {
        'time':         'Time (s)',
        'pos':          'Position (ft)',
        'vel':          'Velocity (ft/s)',
        'accel':        'Acceleration (ft/s/s)',
        'current':      'Current (dA)',
        'voltage':      'Voltage (V)',
        'energy':       'Energy (mAh)',
        'total_energy': 'Total Energy (mAh)',
        'is_slipping':  'Is Slipping'
    }

    num_lines = min(len(line_types), len(elements_to_plot))

    ax.set(xlabel='time (s)', title='Subsystem Acceleration Model')
    ax.grid()
    for i in range(len(models)):
        model = models[i]
        t = [e['time'] for e in model.data_points]

        for j in range(num_lines):
            key = elements_to_plot[j]
            line = line_colours[i % len(line_colours)] + line_types[j]
            ax.plot(t, [e[key] for e in model.data_points], line, label=key)

    handles = []
    handles += [patches.Patch(color=line_colours[i],
                              label='{0}x {1} @ {2}:1 - {3}in'.format(
                                      str(models[i].num_motors),
                                      models[i].motors.__class__.__name__,
                                      models[i].gear_ratio,
                                      models[i].effective_diameter))
                for i in range(len(models))]
    handles += [lines.Line2D([], [], color='k', linestyle=line_types[i], label=headers[elements_to_plot[i]])
                for i in range(num_lines)]
    plt.legend(handles=handles)

    plt.show()


def dump_model_csv(model, filename):
    data_points = model.get_data_points()
    headers = model.csv_headers + \
              [(e + "=" + str(model.to_json()[e])) for e in list(model.to_json().keys())] + \
              [(e + "=" + str(model.motor.to_json()[e])) for e in list(model.motor.to_json().keys())]

    csv_lines = [list(e.values()) for e in data_points]
    csv_lines = [[str(format(e, '.5f') if isinstance(e, float) else e) for e in line] for line in csv_lines]
    csv_str = "\n".join(headers + [",".join(e) for e in csv_lines])

    open(filename, "w+").write(csv_str)
