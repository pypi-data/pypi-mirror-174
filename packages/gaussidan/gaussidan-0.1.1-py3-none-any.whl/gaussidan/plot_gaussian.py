from typing import Sequence, Union

import numpy as np
from lmfit.models import GaussianModel

from gaussidan import fit_gaussian


def plot_gaussian(
    data: Union[Sequence[float], np.ndarray],
    bins: Union[int, Union[Sequence[float], np.ndarray]],
    weights: Union[Sequence[float], np.ndarray] = None,
) -> tuple[np.ndarray, np.ndarray]:

    height, mu, sigma = fit_gaussian(data, bins, weights)
    _, bin_edges = np.histogram(data, bins=bins, weights=weights)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    model = GaussianModel()
    y = model.eval(x=bin_centers, amplitude=height, center=mu, sigma=sigma)

    return bin_centers, y
