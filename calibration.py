import numpy as np


# This function is a sklearn.calibration.calibration_curve modification
def calibration_curve(y_true, y_prob, *, n_bins=5, strategy="uniform"):
    y_true = np.array(y_true)
    y_prob = np.array(y_prob)

    if strategy == "quantile":  # Determine bin edges by distribution of data
        quantiles = np.linspace(0, 1, n_bins + 1)
        bins = np.percentile(y_prob, quantiles * 100)
        bins[-1] = bins[-1] + 1e-8

    elif strategy == "uniform":
        bins = np.linspace(0.0, 1.0 + 1e-8, n_bins + 1)

    else:
        raise ValueError(
            "Invalid entry to 'strategy' input. Strategy "
            "must be either 'quantile' or 'uniform'."
        )

    binids = np.digitize(y_prob, bins) - 1

    bin_sums = np.bincount(binids, weights=y_prob, minlength=len(bins))
    bin_true = np.bincount(binids, weights=y_true, minlength=len(bins))
    bin_total = np.bincount(binids, minlength=len(bins))

    nonzero = bin_total != 0
    prob_true = bin_true[nonzero] / bin_total[nonzero]
    prob_pred = bin_sums[nonzero] / bin_total[nonzero]

    return prob_true, prob_pred, bin_total[nonzero]


def overconfidence(y_true, y_pred):
    x = y_pred * y_true + (1 - y_pred) * (1 - y_true)
    return np.mean((x - 1) * (x - 0.5)) / np.mean((x - 0.5) * (x - 0.5))
