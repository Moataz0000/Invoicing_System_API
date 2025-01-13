from django.http import HttpResponse
from .models import Invoice
from .factory.export_factory import InvoiceExportFactory
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Client, Invoice, InvoiceItem
from .serializers import ClientSerializer, InvoiceSerializer, InvoiceItemSerializer
from .paginations import ClientPagination
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated




# class RegisterView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
    

class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = ClientPagination
    permission_classes = [IsAuthenticated]




class InvocieViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('client').all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.select_related('invoice').all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAuthenticated]


def export_invoice(request, invoice_id, format):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    export_strategy = InvoiceExportFactory.get_export_strategy(format)
    
    # Generate the export file
    file = export_strategy.export(invoice)

    # Return the response with the appropriate file type
    if format.lower() == 'pdf':
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    elif format.lower() == 'csv':
        response = HttpResponse(file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.csv"'

    return response