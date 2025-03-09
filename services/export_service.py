from fpdf import FPDF
import os
from datetime import datetime
from models.summarization_request import ExportFormat
import textwrap

class ExportService:
    def __init__(self):
        self.export_dir = "exports"
        os.makedirs(self.export_dir, exist_ok=True)

    def export_summary(self, summary: str, document_type: str, export_format: ExportFormat) -> str:
        """Export the summary to the specified format and return the file path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == ExportFormat.PDF:
            return self._export_to_pdf(summary, document_type, timestamp)
        else:
            return self._export_to_text(summary, document_type, timestamp)

    def _export_to_pdf(self, summary: str, document_type: str, timestamp: str) -> str:
        """Export the summary to PDF format"""
        filename = f"summary_{document_type}_{timestamp}.pdf"
        filepath = os.path.join(self.export_dir, filename)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Document Summary", ln=True, align="C")
        pdf.ln(10)

        # Add metadata
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Document Type: {document_type}", ln=True)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(10)

        # Add summary content
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, "Summary:", ln=True)
        pdf.ln(5)

        # Wrap text to fit page width
        wrapped_text = textwrap.fill(summary, width=75)
        for line in wrapped_text.split('\n'):
            pdf.multi_cell(0, 10, line)

        # Save PDF
        pdf.output(filepath)
        return filepath

    def _export_to_text(self, summary: str, document_type: str, timestamp: str) -> str:
        """Export the summary to text format"""
        filename = f"summary_{document_type}_{timestamp}.txt"
        filepath = os.path.join(self.export_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Document Summary\n")
            f.write(f"==============\n\n")
            f.write(f"Document Type: {document_type}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Summary:\n")
            f.write("--------\n")
            f.write(summary)
        
        return filepath

export_service = ExportService() 