from abc import ABC, abstractmethod
from io import BytesIO



class InvoiceExportStrategy(ABC):
    
    @abstractmethod
    def export(self, invoice) -> BytesIO:
        """
        Export the invoice to the desired format (e.g., PDF, CSV).
        Returns a file-like object containing the export data.
        """
        pass