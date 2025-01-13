from .base_export import InvoiceExportStrategy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from PIL import Image
from django.conf import settings


class PDFExportStrategy(InvoiceExportStrategy):
    def export(self, invoice) -> BytesIO:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Set up fonts and colors
        primary_color = colors.HexColor("#333333")  # Dark gray for text
        accent_color = colors.HexColor("#1E90FF")  # Blue for accents
        p.setFont("Helvetica", 10)

        # Add Business Information at the Top
        p.setFillColor(primary_color)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, height - 50, invoice.business_name)
        p.setFont("Helvetica", 10)
        p.drawString(40, height - 70, invoice.business_website)

        # Add Invoice Title
        p.setFillColor(accent_color)
        p.setFont("Helvetica-Bold", 18)
        p.drawString(40, height - 120, f"Invoice Number #{invoice.invoice_number}")

        # Add Invoice Details
        p.setFillColor(primary_color)
        p.setFont("Helvetica", 10)
        p.drawString(40, height - 150, f"Issue Date: {invoice.issued_date}")
        p.drawString(40, height - 170, f"Due Date: {invoice.due_date}")
        p.drawString(40, height - 190, f"Status: {invoice.status}")

        # Add Client Information
        p.setFont("Helvetica-Bold", 12)
        p.drawString(width - 200, height - 120, "Bill To:")
        p.setFont("Helvetica", 10)
        p.drawString(width - 200, height - 140, invoice.client.name)
        p.drawString(width - 200, height - 160, invoice.client.email)

        # Add a Separator Line
        p.setStrokeColor(accent_color)
        p.setLineWidth(1)
        p.line(40, height - 200, width - 40, height - 200)

        # Table Headers
        y_position = height - 220
        p.setFillColor(accent_color)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(40, y_position, "Item")
        p.drawString(300, y_position, "Quantity")
        p.drawString(400, y_position, "Unit Price")
        p.drawString(500, y_position, "Total")

        # Table Rows
        y_position -= 20
        total_amount = 0
        p.setFillColor(primary_color)
        p.setFont("Helvetica", 10)

        for item in invoice.items.all():
            p.drawString(40, y_position, item.name)
            p.drawString(300, y_position, str(item.quantity))
            p.drawString(400, y_position, f"${item.unit_price:.2f}")
            total = item.quantity * item.unit_price
            p.drawString(500, y_position, f"${total:.2f}")
            total_amount += total
            y_position -= 20

        # Add Total Amount
        p.setFont("Helvetica-Bold", 12)
        p.drawString(400, y_position - 20, "Total:")
        p.drawString(500, y_position - 20, f"${total_amount:.2f}")

        # Add Footer
        p.setFillColor(accent_color)
        p.setFont("Helvetica", 10)
        p.drawCentredString(width / 2, 40, "Thank you for your business!")
        p.drawCentredString(width / 2, 25, f"For questions, contact {invoice.business_name} at {invoice.business_website}")

        # Finalize PDF
        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer