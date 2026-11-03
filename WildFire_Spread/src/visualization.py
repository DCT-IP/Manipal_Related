import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm

def plot_forest(grid, save_path=None):
    """Display the current forest state."""
    cmap = ListedColormap([
    "black",       # BURNT = -1
    "darkgreen",   # HEALTHY = 0
    "orangered"    # BURNING = 1
])
    # State values are -1, 0 and 1.
    norm = BoundaryNorm([-1.5, -0.5, 0.5, 1.5], cmap.N)
    fig, ax = plt.subplots(figsize=(8, 7))
    image = ax.imshow(grid, cmap=cmap, norm=norm)
    ax.set_title("Wildfire Simulation")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    colorbar = fig.colorbar(image, ax=ax, ticks=[-1, 0, 1])
    colorbar.ax.set_yticklabels(["Burnt", "Healthy", "Burning"])
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=200)
    plt.show()


def plot_burn_probability(probability, save_path=None):
    """Display the probability of each cell burning."""
    fig, ax = plt.subplots(figsize=(8, 7))
    image = ax.imshow(
        probability,
        cmap="hot",
        vmin=0,
        vmax=1,
        interpolation="nearest"
    )
    ax.set_title("Wildfire Burn Probability")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("Probability of burning")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=200)
    plt.show()


def plot_burned_area(burned_areas, save_path=None):
    """Display the distribution of burned forest area."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(
        burned_areas,
        bins=20,
        edgecolor="black"
    )
    ax.set_title("Distribution of Burned Forest Area")
    ax.set_xlabel("Burned Area (%)")
    ax.set_ylabel("Number of Simulations")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=200)
    plt.show()
