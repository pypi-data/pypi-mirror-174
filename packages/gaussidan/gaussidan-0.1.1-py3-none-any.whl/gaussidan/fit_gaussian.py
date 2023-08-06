from typing import Sequence, Union

import numpy as np
from lmfit.models import GaussianModel


def fit_gaussian(
    data: Union[Sequence[float], np.ndarray],
    bins: Union[int, Union[Sequence[float], np.ndarray]],
    weights: Union[Sequence[float], np.ndarray] = None,
    errors: bool = False,
) -> tuple[float, float, float]:

    hist, bin_edges = np.histogram(data, bins=bins, weights=weights)

    mask = np.nonzero(hist)
    hist = hist[mask]
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_centers = bin_centers[mask]

    model = GaussianModel()
    pars = model.guess(hist, x=bin_centers)
    result = model.fit(hist, pars, x=bin_centers)
    # results = out.best_values
    amplitude, center, sigma = (
        result.params["amplitude"],
        result.params["center"],
        result.params["sigma"],
    )
    if errors:
        return (
            (amplitude.value, amplitude.stderr),
            (center.value, center.stderr),
            (sigma.value, sigma.stderr),
        )
    return amplitude.value, center.value, sigma.value
