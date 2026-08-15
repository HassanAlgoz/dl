import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_data(X, y, title="Delivery Data"):
    """
    Creates a scatter plot of the data points.

    Args:
        X: The input data points for the x-axis (distances).
        y: The target data points for the y-axis (times).
        title: Plot title.
    """
    x_plot = np.asarray(X).flatten()
    y_plot = np.asarray(y).flatten()

    plt.figure(figsize=(8, 6))
    plt.plot(
        x_plot,
        y_plot,
        color="orange",
        marker="o",
        linestyle="none",
        label="Actual Delivery Times",
    )
    plt.title(title)
    plt.xlabel("Distance (miles)")
    plt.ylabel("Time (minutes)")
    plt.legend()
    plt.grid(True)
    plt.show()


def _relu_bend_locations(model, x_min, x_max):
    """Return in-range ReLU hinge points for a 1D MLP, in original x units."""
    scaler = None
    mlp = model
    if hasattr(model, "named_steps"):
        scaler = model.named_steps.get("scaler")
        mlp = model.named_steps.get("mlp", model)

    if getattr(mlp, "activation", None) != "relu":
        return []
    if not hasattr(mlp, "coefs_") or len(mlp.coefs_) < 2:
        return []

    weights = np.asarray(mlp.coefs_[0]).flatten()
    biases = np.asarray(mlp.intercepts_[0]).flatten()
    bends = []
    for weight, bias in zip(weights, biases):
        if abs(weight) < 1e-12:
            continue
        x_scaled = -bias / weight
        if scaler is not None:
            x_bend = x_scaled * scaler.scale_[0] + scaler.mean_[0]
        else:
            x_bend = x_scaled
        if x_min <= x_bend <= x_max:
            bends.append(float(x_bend))
    return sorted(bends)


def plot_fit(
    model,
    X,
    y,
    title="Model Fit vs. Actual Data",
    pred_label="Model Predictions",
    mark_bends=False,
):
    """
    Plots the predictions of a trained model against the original data.

    Args:
        model: The trained model used for prediction (must implement predict).
        X: The original input data.
        y: The original target data.
        title: Plot title.
        pred_label: Legend label for the prediction line.
        mark_bends: If True, draw a vertical line at each in-range ReLU hinge.
    """
    x_plot = np.asarray(X).flatten()
    y_plot = np.asarray(y).flatten()
    x_line = np.linspace(x_plot.min(), x_plot.max(), 400)
    if hasattr(X, "columns"):
        X_line = pd.DataFrame(x_line.reshape(-1, 1), columns=list(X.columns))
    else:
        X_line = x_line.reshape(-1, 1)
    y_pred = np.asarray(model.predict(X_line)).flatten()

    plt.figure(figsize=(8, 6))
    plt.plot(
        x_plot,
        y_plot,
        color="orange",
        marker="o",
        linestyle="none",
        label="Actual Data",
    )
    plt.plot(
        x_line,
        y_pred,
        color="green",
        label=pred_label,
    )
    if mark_bends:
        bends = _relu_bend_locations(model, x_plot.min(), x_plot.max())
        for i, x_bend in enumerate(bends):
            plt.axvline(
                x_bend,
                color="steelblue",
                linestyle="--",
                linewidth=1.5,
                alpha=0.85,
                label="ReLU bends" if i == 0 else None,
            )
    plt.title(title)
    plt.xlabel("Distance (miles)")
    plt.ylabel("Time (minutes)")
    plt.legend()
    plt.grid(True)
    plt.show()
