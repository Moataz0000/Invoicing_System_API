from invoices.strategies.pdf_export import PDFExportStrategy
from invoices.strategies.csv_export import CSVExportStrategy



class InvoiceExportFactory:
    @staticmethod
    def get_export_strategy(format: str):
        if format.lower() == 'pdf':
            return PDFExportStrategy()
        elif format.lower() == 'csv':
            return CSVExportStrategy()
        else: 
            raise ValueError('Unsupported format')