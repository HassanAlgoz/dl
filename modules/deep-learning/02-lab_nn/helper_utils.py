import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_regression_data(X, y, title="Regression Data", xlabel="x", ylabel="y"):
    """Scatter plot of a 1D feature against a continuous target."""
    x_plot = np.asarray(X).flatten()
    y_plot = np.asarray(y).flatten()

    plt.figure(figsize=(8, 6))
    plt.plot(
        x_plot,
        y_plot,
        color="orange",
        marker="o",
        linestyle="none",
        label="Data points",
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def plot_fit(
    model,
    X,
    y,
    title="Model Fit vs. Actual Data",
    xlabel="x",
    ylabel="y",
    pred_label="Predicted Line",
):
    """Plot a trained regressor's predictions against 1D data."""
    x_plot = np.asarray(X).flatten()
    y_plot = np.asarray(y).flatten()
    y_pred = np.asarray(model.predict(X)).flatten()
    order = np.argsort(x_plot)

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
        x_plot[order],
        y_pred[order],
        color="green",
        label=pred_label,
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def _xy(X):
    """Return the two feature columns as 1D arrays."""
    values = np.asarray(X)
    return values[:, 0], values[:, 1]


def _grid_frame(X, xx, yy):
    """Build a prediction grid that matches the column names used in training."""
    grid = np.c_[xx.ravel(), yy.ravel()]
    if hasattr(X, "columns"):
        return pd.DataFrame(grid, columns=list(X.columns))
    return grid


def plot_data(X, y, title="Classification Data"):
    """Scatter plot of 2D points colored by class."""
    x0, x1 = _xy(X)
    y_plot = np.asarray(y).ravel()

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        x0,
        x1,
        c=y_plot,
        cmap="coolwarm",
        edgecolors="k",
    )
    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.colorbar(scatter, label="Class (0 or 1)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def _draw_boundary(ax, model, X, y, title):
    x0, x1 = _xy(X)
    y_plot = np.asarray(y).ravel()

    pad = 0.5
    xx, yy = np.meshgrid(
        np.linspace(x0.min() - pad, x0.max() + pad, 200),
        np.linspace(x1.min() - pad, x1.max() + pad, 200),
    )
    preds = np.asarray(model.predict(_grid_frame(X, xx, yy))).reshape(xx.shape)

    ax.contourf(xx, yy, preds, alpha=0.5, cmap="coolwarm")
    ax.scatter(x0, x1, c=y_plot, edgecolors="k", cmap="coolwarm")
    ax.set_title(title)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")


def plot_decision_boundary(model, X, y, title="Decision Boundary"):
    """Plot a trained classifier's decision regions over the 2D data."""
    fig, ax = plt.subplots(figsize=(8, 6))
    _draw_boundary(ax, model, X, y, title)
    plt.show()


def plot_decision_boundaries(models, X, y, titles):
    """Side-by-side decision boundaries for comparing architectures."""
    fig, axes = plt.subplots(1, len(models), figsize=(6 * len(models), 5))
    if len(models) == 1:
        axes = [axes]
    for ax, model, title in zip(axes, models, titles):
        _draw_boundary(ax, model, X, y, title)
    plt.tight_layout()
    plt.show()
