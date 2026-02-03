"""Chart generation utilities using matplotlib.

Provides templates for common financial charts:
- Line charts (trends)
- Bar charts (comparisons)
- Pie charts (compositions)
- Waterfall charts (breakdowns)
"""

from typing import List, Dict, Tuple, Optional, Any
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import numpy as np
from datetime import datetime


# Default styling
COLORS = {
    "primary": "#2E75B6",      # Blue
    "secondary": "#ED7D31",    # Orange
    "success": "#70AD47",      # Green
    "warning": "#FFC000",      # Yellow
    "danger": "#C5504D",       # Red
    "neutral": "#595959",      # Dark gray
}

CHART_STYLE = {
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.facecolor": "white",
    "axes.facecolor": "#F5F5F5",
}


def _setup_style():
    """Apply chart styling."""
    for key, value in CHART_STYLE.items():
        plt.rcParams[key] = value


def _currency_formatter(x, pos):
    """Format axis labels as currency."""
    if x >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    elif x >= 1_000:
        return f"${x/1_000:.0f}K"
    else:
        return f"${x:,.0f}"


def _percentage_formatter(x, pos):
    """Format axis labels as percentage."""
    return f"{x:.0f}%"


def line_chart(
    labels: List[str],
    data_series: Dict[str, List[float]],
    title: str,
    ylabel: str = "Value",
    currency: bool = False,
    figsize: Tuple[int, int] = (10, 6),
) -> BytesIO:
    """Generate a line chart.

    Args:
        labels: X-axis labels (e.g., months)
        data_series: Dictionary of {series_name: [values]}
        title: Chart title
        ylabel: Y-axis label
        currency: Whether to format Y-axis as currency
        figsize: Figure size (width, height)

    Returns:
        BytesIO object containing the PNG image
    """
    _setup_style()

    fig, ax = plt.subplots(figsize=figsize, dpi=100)

    # Plot each data series
    colors_list = list(COLORS.values())
    for idx, (series_name, values) in enumerate(data_series.items()):
        color = colors_list[idx % len(colors_list)]
        ax.plot(
            labels,
            values,
            marker="o",
            linewidth=2.5,
            label=series_name,
            color=color,
            markersize=6
        )

    ax.set_xlabel("")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_title(title, fontweight="bold", fontsize=14, pad=20)

    # Format Y-axis
    if currency:
        ax.yaxis.set_major_formatter(FuncFormatter(_currency_formatter))
    else:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{x:,.0f}"))

    # Grid and legend
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="best", frameon=True, fancybox=True)

    # Rotate x-axis labels if needed
    if len(labels) > 12:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    # Export to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close()

    return buf


def bar_chart(
    labels: List[str],
    values: List[float],
    title: str,
    ylabel: str = "Value",
    currency: bool = False,
    colors: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 6),
) -> BytesIO:
    """Generate a bar chart.

    Args:
        labels: Bar labels
        values: Bar values
        title: Chart title
        ylabel: Y-axis label
        currency: Whether to format Y-axis as currency
        colors: List of colors for bars
        figsize: Figure size (width, height)

    Returns:
        BytesIO object containing the PNG image
    """
    _setup_style()

    fig, ax = plt.subplots(figsize=figsize, dpi=100)

    if colors is None:
        colors = [COLORS["primary"]] * len(labels)

    bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.5)

    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_title(title, fontweight="bold", fontsize=14, pad=20)

    # Format Y-axis
    if currency:
        ax.yaxis.set_major_formatter(FuncFormatter(_currency_formatter))
    else:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{x:,.0f}"))

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height != 0:
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f"{height:,.0f}" if not currency else f"${height/1_000_000:.1f}M",
                ha="center",
                va="bottom" if height > 0 else "top",
                fontsize=9
            )

    # Rotate x-axis labels if needed
    if len(labels) > 12:
        plt.xticks(rotation=45, ha="right")

    ax.grid(True, alpha=0.3, axis="y", linestyle="--")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close()

    return buf


def waterfall_chart(
    categories: List[str],
    values: List[float],
    title: str,
    start_label: str = "Start",
    end_label: str = "End",
    figsize: Tuple[int, int] = (12, 6),
) -> BytesIO:
    """Generate a waterfall chart showing value flow.

    Args:
        categories: Category names
        values: Category values (positive/negative)
        title: Chart title
        start_label: Label for starting balance
        end_label: Label for ending balance
        figsize: Figure size (width, height)

    Returns:
        BytesIO object containing the PNG image
    """
    _setup_style()

    fig, ax = plt.subplots(figsize=figsize, dpi=100)

    # Calculate cumulative values for positioning
    cumulative = 0
    positions = []
    bar_values = []
    colors = []

    # Add starting position
    positions.append(0)
    bar_values.append(values[0])
    colors.append(COLORS["primary"])
    cumulative = values[0]

    # Add middle values
    for i in range(1, len(values) - 1):
        positions.append(cumulative)
        bar_values.append(values[i])
        colors.append(COLORS["secondary"] if values[i] >= 0 else COLORS["danger"])
        cumulative += values[i]

    # Add ending position
    positions.append(0)
    bar_values.append(cumulative)
    colors.append(COLORS["success"])

    # Create bars
    x_pos = range(len(categories))
    bars = ax.bar(x_pos, bar_values, bottom=positions, color=colors, edgecolor="black", linewidth=0.5)

    # Add connecting lines
    for i in range(len(categories) - 1):
        if i == 0:
            next_pos = values[0] + values[1]
        else:
            next_pos = positions[i] + bar_values[i]

        ax.plot([i + 0.4, i + 0.6], [next_pos, next_pos], "k-", linewidth=1)

    # Format and labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.set_title(title, fontweight="bold", fontsize=14, pad=20)
    ax.yaxis.set_major_formatter(FuncFormatter(_currency_formatter))

    ax.grid(True, alpha=0.3, axis="y", linestyle="--")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close()

    return buf


def pie_chart(
    labels: List[str],
    values: List[float],
    title: str,
    figsize: Tuple[int, int] = (8, 8),
) -> BytesIO:
    """Generate a pie chart.

    Args:
        labels: Slice labels
        values: Slice values
        title: Chart title
        figsize: Figure size (width, height)

    Returns:
        BytesIO object containing the PNG image
    """
    _setup_style()

    fig, ax = plt.subplots(figsize=figsize, dpi=100)

    colors_list = list(COLORS.values())
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors_list,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 10}
    )

    ax.set_title(title, fontweight="bold", fontsize=14, pad=20)

    # Improve text readability
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close()

    return buf


def scatter_chart(
    x_values: List[float],
    y_values: List[float],
    labels: List[str] = None,
    title: str = "Scatter Plot",
    xlabel: str = "X",
    ylabel: str = "Y",
    figsize: Tuple[int, int] = (10, 6),
) -> BytesIO:
    """Generate a scatter plot.

    Args:
        x_values: X-axis values
        y_values: Y-axis values
        labels: Optional labels for each point
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height)

    Returns:
        BytesIO object containing the PNG image
    """
    _setup_style()

    fig, ax = plt.subplots(figsize=figsize, dpi=100)

    ax.scatter(x_values, y_values, s=100, color=COLORS["primary"], alpha=0.6, edgecolor="black")

    if labels:
        for i, label in enumerate(labels):
            ax.annotate(label, (x_values[i], y_values[i]), fontsize=8, alpha=0.7)

    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_title(title, fontweight="bold", fontsize=14, pad=20)

    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close()

    return buf
