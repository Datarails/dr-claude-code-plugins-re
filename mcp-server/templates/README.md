# Report Templates

This directory contains templates and styling configuration for generating professional financial reports.

## Structure

- `chart_styles.json` - Color schemes and styling defaults for all report formats

## Customization

### Color Schemes

Three pre-built color schemes are available:

1. **default** - Professional blue and orange scheme
2. **warm** - Warm earth tones
3. **cool** - Cool blue and green scheme

To use a custom color scheme, modify `chart_styles.json` and add your own palette under `color_schemes`.

### Chart Styling

Chart generation can be customized via `chart_defaults`:

```json
{
  "chart_defaults": {
    "dpi": 100,
    "figsize": {"small": [8, 6], "medium": [10, 7], "large": [12, 8]},
    "fonts": {"family": "sans-serif", "title_size": 14},
    "grid": {"enabled": true, "alpha": 0.3}
  }
}
```

### Excel Report Styling

Customize Excel output with `excel_defaults`:

- `header_fill` - Header background color (hex)
- `header_font_color` - Header text color (hex)
- `border_style` - Cell border style (thin, medium, thick)
- `freeze_panes` - Default freeze position

### PowerPoint Styling

Customize presentations with `powerpoint_defaults`:

- Colors and fonts for all slide elements
- Default slide dimensions
- Font sizes for titles, headings, and body text

### PDF Styling

Customize PDF reports with `pdf_defaults`:

- Page size and margins
- Header styling
- Table formatting options

## Usage in Agents

Agents load and apply templates automatically:

```python
import json
from pathlib import Path

# Load styling configuration
templates_dir = Path(__file__).parent.parent / "templates"
with open(templates_dir / "chart_styles.json") as f:
    styles = json.load(f)

# Use in chart generation
color_scheme = styles["color_schemes"]["default"]
chart_config = styles["chart_defaults"]
```

## Future Enhancements

- Pre-built PowerPoint templates (.pptx)
- PDF header/footer customization
- Data validation rules for Excel
- Chart template presets
- Localization support (multiple languages)
