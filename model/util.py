import matplotlib.pyplot as plt
from matplotlib import lines, patches


def plot_models(*models):
    fig, ax = plt.subplots()

    ax.set(xlabel='time (s)', title='Subsystem Acceleration Model')
    ax.grid()
    for i in range(len(models)):
        model = models[i]
        t = [e[0] for e in [list(e.values()) for e in model.data_points][1:]]
        for j in range(len(model.line_types)):
            if j not in model.elements_to_plot:
                continue
            line = model.line_colours[i % len(model.line_colours)] + model.line_types[j]
            ax.plot(t, [e[j + 1] for e in [list(e.values()) for e in model.data_points][1:]], line,
                    label=model.csv_headers[j + 1])

    handles = []
    handles += [patches.Patch(color=models[i].line_colours[i],
                              label='{0}x {1} @ {2}:1 - {3}in'.format(
                                      str(models[i].num_motors),
                                      models[i].motor_type,
                                      models[i].gear_ratio,
                                      models[i].effective_diameter))
                for i in range(len(models))]
    handles += [lines.Line2D([], [], color='k', linestyle=models[0].line_types[i], label=models[0].csv_headers[i + 1])
                for i in range(len(models[0].line_types)) if i in models[0].elements_to_plot]
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
