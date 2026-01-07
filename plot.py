import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from linear import milp_model
from utils import expand_index


def save_plot(prime, m, threshold, num, seed=0):
    indices = milp_model(prime, m, threshold, seed)[1]
    points = [expand_index(index, prime) for index in indices]
    array_points = np.array(points)
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(projection="3d")

    ax.set_xlim(0, prime - 1)
    ax.set_ylim(0, prime - 1)
    ax.set_zlim(0, prime - 1)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.zaxis.set_major_locator(MaxNLocator(integer=True))

    ax.view_init(elev=22, azim=41)

    ax.scatter(
        array_points[:, 0],
        array_points[:, 1],
        array_points[:, 2],
        s=40,
        color="black",
        depthshade=False,
        alpha=1.0,
    )
    ax.set_box_aspect([1, 1, 1])
    plt.tight_layout()
    plt.savefig(f"images/plot_{num:02d}.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    for i in range(50):
        save_plot(5, 2, 10, i, i)
