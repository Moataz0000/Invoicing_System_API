import csv
from io import StringIO
from .base_export import InvoiceExportStrategy

class CSVExportStrategy(InvoiceExportStrategy):
    def export(self, invoice) -> StringIO:
        output = StringIO()
        writer = csv.writer(output)
        
        # Header row with business information
        writer.writerow(['Business Name', 'Business Website', 'Invoice Number', 'Client Name', 'Issue Date', 'Due Date', 'Status'])
        writer.writerow([
            invoice.business_name,
            invoice.business_website,
            invoice.invoice_number,
            invoice.client.name,
            invoice.issued_date,
            invoice.due_date,
            invoice.status,
        ])

        # Add a blank row for separation
        writer.writerow([])

        # Header row for items
        writer.writerow(['Name', 'Quantity', 'Unit Price', 'Total'])

        # Invoice items
        for item in invoice.items.all():
            writer.writerow([item.name, item.quantity, item.unit_price, item.quantity * item.unit_price])

        # Write the total at the end
        total = sum(item.quantity * item.unit_price for item in invoice.items.all())
        writer.writerow(['', '', 'Total', total])

        output.seek(0)
        return output