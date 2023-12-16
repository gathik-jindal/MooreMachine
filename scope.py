from matplotlib import pyplot as plt


def plot(inputs: dict):
    """
    plots the wave forms in a single window that are supplied in form of a dict.
    """

    n_rows = len(inputs)
    n_cols = 1

    plt.title('Waveforms')
    counter = 1
    for key in inputs:
        x_axis = [y[0] for y in inputs[key]]
        y_axis = [y[1] for y in inputs[key]]
        x_ticks = range(0, int(x_axis[-1]) + 1, 1)

        plt.subplot(n_rows, n_cols, counter)
        counter += 1
        plt.step(x_axis, y_axis, where='post')
        plt.ylabel(key)
        plt.xticks(x_ticks)
        plt.grid(True)

    plt.xlabel('Time (units)')
    plt.tight_layout()
    plt.show()