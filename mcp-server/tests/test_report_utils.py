"""Tests for report_utils module."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datarails_mcp.report_utils import (
    format_currency,
    format_percentage,
    format_ratio,
    format_number,
    calculate_growth_rate,
    calculate_variance,
    get_severity_color,
    get_severity_level,
    summarize_anomalies,
    safe_divide,
)


class TestCurrencyFormatting:
    """Tests for currency formatting."""

    def test_format_currency_millions(self):
        """Test formatting millions."""
        assert format_currency(1_500_000) == "$1.5M"
        assert format_currency(5_000_000, decimals=2) == "$5.00M"

    def test_format_currency_thousands(self):
        """Test formatting thousands."""
        assert format_currency(45_000) == "$45K"
        assert format_currency(1_234.56, decimals=2) == "$1.23K"

    def test_format_currency_dollars(self):
        """Test formatting dollars."""
        assert format_currency(234.56, decimals=2) == "$234.56"
        assert format_currency(1234) == "$1,234"

    def test_format_currency_negative(self):
        """Test formatting negative values."""
        assert format_currency(-1_500_000) == "$-1.5M"

    def test_format_currency_no_symbol(self):
        """Test formatting without symbol."""
        assert format_currency(1_500_000, include_symbol=False) == "1.5M"

    def test_format_currency_none(self):
        """Test formatting None."""
        assert format_currency(None) == "—"


class TestPercentageFormatting:
    """Tests for percentage formatting."""

    def test_format_percentage_decimal(self):
        """Test formatting decimal percentages."""
        assert format_percentage(0.45) == "45.0%"
        assert format_percentage(0.123, decimals=2) == "12.30%"

    def test_format_percentage_integer(self):
        """Test formatting integer percentages."""
        assert format_percentage(45) == "45.0%"
        assert format_percentage(45.67, decimals=2) == "45.67%"

    def test_format_percentage_negative(self):
        """Test formatting negative percentages."""
        assert format_percentage(-0.15) == "-15.0%"


class TestRatioFormatting:
    """Tests for ratio formatting."""

    def test_format_ratio(self):
        """Test formatting ratios."""
        assert format_ratio(1.23) == "1.23x"
        assert format_ratio(2.5, decimals=1) == "2.5x"
        assert format_ratio(0.75) == "0.75x"


class TestNumberFormatting:
    """Tests for general number formatting."""

    def test_format_number(self):
        """Test formatting numbers."""
        assert format_number(1234567) == "1,234,567"
        assert format_number(1234.567, decimals=2) == "1,234.57"


class TestGrowthRateCalculation:
    """Tests for growth rate calculation."""

    def test_calculate_growth_rate_positive(self):
        """Test calculating positive growth."""
        rate = calculate_growth_rate(150, 100)
        assert rate == 0.5  # 50% growth

    def test_calculate_growth_rate_negative(self):
        """Test calculating negative growth."""
        rate = calculate_growth_rate(80, 100)
        assert rate == -0.2  # -20% growth

    def test_calculate_growth_rate_zero_previous(self):
        """Test growth from zero."""
        rate = calculate_growth_rate(100, 0)
        assert rate == float('inf')

    def test_calculate_growth_rate_no_change(self):
        """Test no growth."""
        rate = calculate_growth_rate(100, 100)
        assert rate == 0


class TestVarianceCalculation:
    """Tests for variance calculation."""

    def test_calculate_variance_positive(self):
        """Test positive variance."""
        variance = calculate_variance(150, 100)
        assert variance["absolute"] == 50
        assert variance["percentage"] == 0.5

    def test_calculate_variance_negative(self):
        """Test negative variance."""
        variance = calculate_variance(80, 100)
        assert variance["absolute"] == -20
        assert variance["percentage"] == -0.2

    def test_calculate_variance_zero_budget(self):
        """Test variance with zero budget."""
        variance = calculate_variance(50, 0)
        assert variance["percentage"] == 0


class TestSeverityColor:
    """Tests for severity color mapping."""

    def test_get_severity_color_critical(self):
        """Test critical severity color."""
        color = get_severity_color("critical")
        assert color == (192, 0, 0)

    def test_get_severity_color_high(self):
        """Test high severity color."""
        color = get_severity_color("high")
        assert color == (255, 192, 0)

    def test_get_severity_color_unknown(self):
        """Test unknown severity."""
        color = get_severity_color("unknown")
        assert color == (128, 128, 128)


class TestSeverityLevel:
    """Tests for severity level determination."""

    def test_get_severity_level_critical(self):
        """Test critical threshold."""
        level = get_severity_level(100, 80, 50, 20)
        assert level == "critical"

    def test_get_severity_level_high(self):
        """Test high threshold."""
        level = get_severity_level(60, 80, 50, 20)
        assert level == "high"

    def test_get_severity_level_medium(self):
        """Test medium threshold."""
        level = get_severity_level(30, 80, 50, 20)
        assert level == "medium"

    def test_get_severity_level_low(self):
        """Test low threshold."""
        level = get_severity_level(10, 80, 50, 20)
        assert level == "low"


class TestAnomalySummarization:
    """Tests for anomaly summarization."""

    def test_summarize_anomalies_empty(self):
        """Test summarizing empty anomalies."""
        result = summarize_anomalies([])
        assert result["total"] == 0
        assert result["data_quality_score"] == 100

    def test_summarize_anomalies_with_findings(self):
        """Test summarizing anomalies with findings."""
        anomalies = [
            {"severity": "critical"},
            {"severity": "critical"},
            {"severity": "high"},
            {"severity": "medium"},
        ]
        result = summarize_anomalies(anomalies)
        assert result["total"] == 4
        assert result["by_severity"]["critical"] == 2
        assert result["by_severity"]["high"] == 1
        assert result["data_quality_score"] < 100

    def test_data_quality_score_excellent(self):
        """Test excellent data quality score."""
        anomalies = [{"severity": "low"}, {"severity": "low"}]
        result = summarize_anomalies(anomalies)
        assert result["data_quality_score"] >= 95


class TestSafeDivide:
    """Tests for safe division."""

    def test_safe_divide_normal(self):
        """Test normal division."""
        result = safe_divide(10, 2)
        assert result == 5

    def test_safe_divide_zero_denominator(self):
        """Test division by zero."""
        result = safe_divide(10, 0)
        assert result == 0

    def test_safe_divide_zero_denominator_custom_default(self):
        """Test division by zero with custom default."""
        result = safe_divide(10, 0, default=99)
        assert result == 99

    def test_safe_divide_invalid_types(self):
        """Test division with invalid types."""
        result = safe_divide("a", "b")
        assert result == 0
