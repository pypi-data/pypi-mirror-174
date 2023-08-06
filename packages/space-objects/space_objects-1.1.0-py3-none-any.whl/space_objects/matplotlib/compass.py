from typing import Literal

import numpy as np
from matplotlib import pyplot as plt


def get_x(angle_degree: float):
    return np.pi * angle_degree / 180


def draw_compass(
    angle_degree,
    title,
    direction="N",
    orientation: Literal["H", "V"] = "H",
):
    """
    Simple matplotlib compass drawwing method.
    """
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    ax = plt.subplot(1, 1, 1, projection="polar")
    ax.set_theta_direction(-1)  # type: ignore
    ax.set_yticklabels([])
    if orientation == "V":
        angle_degree = angle_degree - 90
        ax.set_xticklabels(
            [
                "90°",
                "",
                "",
                "",
                "-90°",
                "-45°",
                "0°",
                "45°",
            ]
        )
    else:
        ax.set_xticklabels(
            [
                "N",
                "",
                "E",
                "",
                "S",
                "",
                "W",
                "",
            ]
        )
    ax.set_theta_zero_location(direction)  # type: ignore
    ax.grid(False)
    ax.arrow(
        x=get_x(angle_degree),
        y=0,
        dx=0,
        dy=1,
        width=0.05,
        facecolor="red",
        edgecolor="none",
    )
    plt.title(title)
    plt.show()
