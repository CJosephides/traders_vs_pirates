"""
viz.py
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_game(game):
    """
    Plot the score time series for a single game.
    """

    # TODO: Validation checks go here.
    if not hasattr(game, 'result_ts'):
        raise Exception('Game instance does not have a result.')

    fig, ax = plt.subplots(1, 1)
    ax.grid()
    for i in range(len(game.result_ts)):
        ax.plot(game.result_ts[i]['scores'],
                label=game.result_ts[i]['strategy'])

    ax.legend(loc='upper left', title='player\nstrategy',
              fontsize=10)
    ax.set_xlabel('turns', fontsize=11)
    ax.set_ylabel('score', fontsize=11)
    ax.set_title('game time series', fontsize=11)
    plt.show()


def plot_pit(pit):
    """
    Plot pit time series, showing median and IQ ranges.
    """

    # Set up some colors.
    colors = [(0.984313725490196, 0.7058823529411765, 0.6823529411764706),
              (0.7019607843137254, 0.803921568627451, 0.8901960784313725),
              (0.8, 0.9215686274509803, 0.7725490196078432),
              (0.8705882352941177, 0.796078431372549, 0.8941176470588236),
              (0.996078431372549, 0.8509803921568627, 0.6509803921568628),
              (1.0, 1.0, 0.8),
              (0.8980392156862745, 0.8470588235294118, 0.7411764705882353),
              (0.9921568627450981, 0.8549019607843137, 0.9254901960784314)]

    # Gather time series in a list of matrices
    matrix_list = []

    # For each game, construct the matrix of time series.
    for game in pit.outcomes:
        ts_matrix = []
        for pr in game:
            ts_matrix.append(pr['scores'])
        ts_matrix = np.array(ts_matrix)
        matrix_list.append(ts_matrix)

    # Get an n_games X n_players X n_times array.
    matrix_list = np.array(matrix_list)

    ts_means = np.transpose(np.mean(matrix_list, axis=0))
    ts_std = np.transpose(np.std(matrix_list, axis=0))

    fig, ax = plt.subplots(1, 1)
    ax.grid(axis='x')
    for i in range(np.shape(ts_means)[1]):
        ax.plot(np.arange(np.shape(ts_means)[0]),
                ts_means[:, i], color=colors[i],
                linewidth=3,
                label=pit.compete_strats[i].name)

        ax.fill_between(np.arange(np.shape(ts_means)[0]),
                        ts_means[:, i] + ts_std[:, i],
                        ts_means[:, i] - ts_std[:, i],
                        color=colors[i],
                        alpha=0.2)

        ax.plot(np.arange(np.shape(ts_means)[0]),
                ts_means[:, i] + ts_std[:, i],
                color=colors[i],
                linewidth=1,
                alpha=0.75)

        ax.plot(np.arange(np.shape(ts_means)[0]),
                ts_means[:, i] - ts_std[:, i],
                color=colors[i],
                linewidth=1,
                alpha=0.6)

    ax.legend(loc='upper left', title='player\nstrategy', fontsize=10)
    ax.set_xlabel('turns', fontsize=11)
    ax.set_ylabel('score (mean +/- std)', fontsize=11)
    ax.set_title('pit results (over %d games)' % len(pit.outcomes),
                 fontsize=11)
    plt.show()
