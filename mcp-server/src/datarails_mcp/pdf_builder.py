"""PDF report generation utilities.

Provides templates for creating professional PDF reports with
formatting, tables, and styling.
"""

from typing import List, Dict, Tuple, Optional, Any
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image as RLImage
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class PDFReport:
    """Builder for creating PDF reports."""

    def __init__(self, title: str = "Report", filename: str = None,
                 pagesize: str = "letter"):
        """Initialize PDF report builder.

        Args:
            title: Report title
            filename: Output filename (if None, use BytesIO)
            pagesize: Page size (letter or a4)
        """
        self.title = title
        self.filename = filename
        self.pagesize = letter if pagesize.lower() == "letter" else A4
        self.story = []
        self._setup_styles()

    def _setup_styles(self):
        """Setup report styles."""
        styles = getSampleStyleSheet()

        # Define custom styles
        self.styles = {
            "title": ParagraphStyle(
                "Title",
                parent=styles["Heading1"],
                fontSize=28,
                textColor=colors.HexColor("2E75B6"),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold"
            ),
            "heading1": ParagraphStyle(
                "Heading1",
                parent=styles["Heading1"],
                fontSize=18,
                textColor=colors.HexColor("2E75B6"),
                spaceAfter=12,
                fontName="Helvetica-Bold"
            ),
            "heading2": ParagraphStyle(
                "Heading2",
                parent=styles["Heading2"],
                fontSize=14,
                textColor=colors.HexColor("4472C4"),
                spaceAfter=8,
                fontName="Helvetica-Bold"
            ),
            "heading3": ParagraphStyle(
                "Heading3",
                parent=styles["Heading3"],
                fontSize=12,
                textColor=colors.HexColor("595959"),
                spaceAfter=6,
                fontName="Helvetica-Bold"
            ),
            "normal": styles["Normal"],
            "body": ParagraphStyle(
                "Body",
                parent=styles["Normal"],
                fontSize=10,
                leading=14,
                spaceAfter=6
            ),
            "critical": ParagraphStyle(
                "Critical",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("C5504D"),
                fontName="Helvetica-Bold"
            ),
            "high": ParagraphStyle(
                "High",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("ED7D31")
            ),
            "medium": ParagraphStyle(
                "Medium",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("F8B500")
            ),
            "low": ParagraphStyle(
                "Low",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("595959")
            ),
            "table_header": ParagraphStyle(
                "TableHeader",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.whitesmoke,
                fontName="Helvetica-Bold",
                alignment=TA_CENTER
            ),
            "table_cell": ParagraphStyle(
                "TableCell",
                parent=styles["Normal"],
                fontSize=9,
                valign="MIDDLE"
            ),
        }

    def add_title(self, title: str, subtitle: str = ""):
        """Add title section.

        Args:
            title: Title text
            subtitle: Optional subtitle
        """
        self.story.append(Paragraph(title, self.styles["title"]))
        if subtitle:
            self.story.append(Paragraph(subtitle, self.styles["body"]))
        self.story.append(Spacer(1, 0.3 * inch))

    def add_heading(self, text: str, level: int = 1):
        """Add heading.

        Args:
            text: Heading text
            level: Heading level (1, 2, or 3)
        """
        style_key = f"heading{level}"
        if style_key in self.styles:
            self.story.append(Paragraph(text, self.styles[style_key]))
            self.story.append(Spacer(1, 0.2 * inch))

    def add_paragraph(self, text: str):
        """Add paragraph of text.

        Args:
            text: Paragraph text
        """
        self.story.append(Paragraph(text, self.styles["body"]))
        self.story.append(Spacer(1, 0.1 * inch))

    def add_bullet_points(self, items: List[str]):
        """Add bullet points.

        Args:
            items: List of bullet point texts
        """
        for item in items:
            para = Paragraph(f"• {item}", self.styles["body"])
            self.story.append(para)
        self.story.append(Spacer(1, 0.1 * inch))

    def add_table(self, data: List[List[str]], header_row: bool = True,
                  col_widths: Optional[List[float]] = None):
        """Add table to report.

        Args:
            data: 2D list of cell values
            header_row: Whether first row is header
            col_widths: Optional list of column widths
        """
        if not data:
            return

        # Convert data to paragraphs for proper formatting
        table_data = []
        for row_idx, row in enumerate(data):
            table_row = []
            for cell_value in row:
                if row_idx == 0 and header_row:
                    p = Paragraph(str(cell_value), self.styles["table_header"])
                else:
                    p = Paragraph(str(cell_value), self.styles["table_cell"])
                table_row.append(p)
            table_data.append(table_row)

        # Create table
        if col_widths:
            table = Table(table_data, colWidths=col_widths)
        else:
            table = Table(table_data)

        # Apply styling
        style_commands = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("2E75B6")) if header_row else None,
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke) if header_row else None,
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold") if header_row else None,
            ("FONTSIZE", (0, 0), (-1, 0), 10) if header_row else None,
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12) if header_row else None,
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("F5F5F5")]),
        ]

        table.setStyle(TableStyle([cmd for cmd in style_commands if cmd]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))

    def add_severity_table(self, findings: List[Dict[str, str]]):
        """Add findings table with severity coloring.

        Args:
            findings: List of {severity, title, description}
        """
        if not findings:
            return

        data = [["Severity", "Finding", "Description"]]

        for finding in findings:
            severity = finding.get("severity", "medium").upper()
            title = finding.get("title", "")
            description = finding.get("description", "")
            data.append([severity, title, description])

        # Create table with severity colors
        table_data = []
        severity_colors = {
            "CRITICAL": colors.HexColor("F4B183"),
            "HIGH": colors.HexColor("FCE4D6"),
            "MEDIUM": colors.HexColor("FFFFE0"),
            "LOW": colors.HexColor("E2EFDA"),
        }

        for row_idx, row in enumerate(data):
            table_row = []
            for cell_value in row:
                p = Paragraph(str(cell_value), self.styles["table_header" if row_idx == 0 else "table_cell"])
                table_row.append(p)
            table_data.append(table_row)

        table = Table(table_data, colWidths=[1.2*inch, 2.5*inch, 2.5*inch])

        # Build style commands
        style_commands = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("2E75B6")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]

        # Apply severity row colors
        for row_idx in range(1, len(data)):
            severity = data[row_idx][0].upper()
            bg_color = severity_colors.get(severity, colors.white)
            style_commands.append(("BACKGROUND", (0, row_idx), (-1, row_idx), bg_color))

        table.setStyle(TableStyle(style_commands))
        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))

    def add_metrics_section(self, metrics: Dict[str, str]):
        """Add metrics section with key-value pairs.

        Args:
            metrics: Dictionary of metric_name: metric_value
        """
        data = []
        for name, value in metrics.items():
            data.append([name + ":", str(value)])

        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("F5F5F5")]),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))

    def add_page_break(self):
        """Add page break."""
        self.story.append(PageBreak())

    def add_footer(self, text: str = ""):
        """Add footer text.

        Args:
            text: Footer text (default: timestamp)
        """
        if not text:
            text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        self.footer_text = text

    def save(self, filepath: str):
        """Save PDF to file.

        Args:
            filepath: Output file path

        Returns:
            File path
        """
        doc = SimpleDocTemplate(
            filepath,
            pagesize=self.pagesize,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        doc.build(self.story)
        return filepath

    def to_bytes(self) -> bytes:
        """Convert to bytes.

        Returns:
            Bytes representation of PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.pagesize,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        doc.build(self.story)
        buffer.seek(0)
        return buffer.getvalue()
