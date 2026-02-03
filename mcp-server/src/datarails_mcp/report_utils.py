"""Shared utilities for report generation.

Provides common formatting, styling, and utility functions used across
all financial report agents.
"""

from typing import Any, List, Dict, Tuple, Optional
from datetime import datetime
import json


def format_currency(value: float, decimals: int = 0, include_symbol: bool = True) -> str:
    """Format a number as currency.

    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default 0)
        include_symbol: Whether to include $ symbol

    Returns:
        Formatted currency string (e.g. "$1.2M", "$45,231.50")
    """
    if value is None:
        return "—"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)

    prefix = "$" if include_symbol else ""

    # Format with thousands separator
    if decimals == 0:
        if abs(value) >= 1_000_000:
            formatted = f"{value / 1_000_000:.1f}M"
        elif abs(value) >= 1_000:
            formatted = f"{value / 1_000:.0f}K"
        else:
            formatted = f"{value:,.0f}"
    else:
        if abs(value) >= 1_000_000:
            formatted = f"{value / 1_000_000:.{decimals}f}M"
        elif abs(value) >= 1_000:
            formatted = f"{value / 1_000:.{decimals}f}K"
        else:
            formatted = f"{value:,.{decimals}f}"

    return f"{prefix}{formatted}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a number as percentage.

    Args:
        value: Numeric value (0-1 or 0-100)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string (e.g. "45.2%")
    """
    if value is None:
        return "—"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)

    # If value is between -1 and 1, assume it's already a decimal
    if -1 <= value <= 1:
        value = value * 100

    return f"{value:.{decimals}f}%"


def format_ratio(value: float, decimals: int = 2) -> str:
    """Format a number as a ratio.

    Args:
        value: Numeric value
        decimals: Number of decimal places

    Returns:
        Formatted ratio string (e.g. "1.23x")
    """
    if value is None:
        return "—"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)

    return f"{value:.{decimals}f}x"


def format_number(value: float, decimals: int = 0) -> str:
    """Format a number with thousands separator.

    Args:
        value: Numeric value
        decimals: Number of decimal places

    Returns:
        Formatted number string
    """
    if value is None:
        return "—"

    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)

    return f"{value:,.{decimals}f}"


def calculate_growth_rate(current: float, previous: float) -> float:
    """Calculate growth rate (current vs previous).

    Args:
        current: Current period value
        previous: Previous period value

    Returns:
        Growth rate as decimal (e.g. 0.15 for 15%)
    """
    if previous == 0:
        return 0 if current == 0 else float('inf')

    return (current - previous) / abs(previous)


def calculate_variance(actual: float, budget: float) -> Dict[str, float]:
    """Calculate variance between actual and budget.

    Args:
        actual: Actual value
        budget: Budget value

    Returns:
        Dictionary with absolute and percentage variance
    """
    absolute = actual - budget
    percentage = (actual / budget - 1) if budget != 0 else 0

    return {
        "absolute": absolute,
        "percentage": percentage,
        "budget": budget,
        "actual": actual
    }


def get_severity_color(severity: str) -> Tuple[int, int, int]:
    """Get RGB color for severity level.

    Args:
        severity: Severity level (critical, high, medium, low, info)

    Returns:
        RGB tuple
    """
    colors = {
        "critical": (192, 0, 0),      # Dark red
        "high": (255, 192, 0),         # Orange
        "medium": (255, 255, 0),       # Yellow
        "low": (192, 192, 192),        # Gray
        "info": (0, 0, 255),           # Blue
        "success": (0, 176, 80),       # Green
    }
    return colors.get(severity.lower(), (128, 128, 128))


def get_severity_level(value: float, threshold_critical: float,
                       threshold_high: float, threshold_medium: float) -> str:
    """Determine severity level based on thresholds.

    Args:
        value: Value to assess
        threshold_critical: Threshold for critical
        threshold_high: Threshold for high
        threshold_medium: Threshold for medium

    Returns:
        Severity level: critical, high, medium, or low
    """
    value = abs(value)

    if value >= threshold_critical:
        return "critical"
    elif value >= threshold_high:
        return "high"
    elif value >= threshold_medium:
        return "medium"
    else:
        return "low"


def summarize_anomalies(anomalies: List[Dict]) -> Dict[str, Any]:
    """Summarize anomaly detection results.

    Args:
        anomalies: List of anomaly dictionaries

    Returns:
        Summary with counts by severity and data quality score
    """
    by_severity = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for anomaly in anomalies:
        severity = anomaly.get("severity", "low").lower()
        if severity in by_severity:
            by_severity[severity] += 1

    total = sum(by_severity.values())

    # Data quality score: 100 - (critical*10 + high*5 + medium*2 + low*0.5)
    score = 100 - (
        by_severity["critical"] * 10 +
        by_severity["high"] * 5 +
        by_severity["medium"] * 2 +
        by_severity["low"] * 0.5
    )
    score = max(0, min(100, score))  # Clamp to 0-100

    return {
        "total": total,
        "by_severity": by_severity,
        "data_quality_score": score,
        "health_status": (
            "🔴 Critical" if score < 70 else
            "🟠 Poor" if score < 80 else
            "🟡 Fair" if score < 90 else
            "🟢 Good" if score < 95 else
            "✅ Excellent"
        )
    }


def flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
    """Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for nested keys

    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i, item in enumerate(v):
                items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """Safely divide two numbers.

    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is 0

    Returns:
        Result of division or default
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default


def get_date_range_label(start_date: Optional[Any], end_date: Optional[Any]) -> str:
    """Generate a readable date range label.

    Args:
        start_date: Start date (string or datetime)
        end_date: End date (string or datetime)

    Returns:
        Formatted date range (e.g. "Jan 2025 - Dec 2025")
    """
    if not start_date or not end_date:
        return "Date range unavailable"

    try:
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.split("T")[0])
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.split("T")[0])

        if start_date.year == end_date.year:
            return f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"
        else:
            return f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"
    except Exception:
        return f"{start_date} - {end_date}"


def export_json(data: Any, filepath: str, pretty: bool = True) -> str:
    """Export data to JSON file.

    Args:
        data: Data to export
        filepath: Output file path
        pretty: Whether to pretty-print JSON

    Returns:
        File path
    """
    with open(filepath, 'w') as f:
        json.dump(
            data,
            f,
            indent=2 if pretty else None,
            default=str
        )

    return filepath
