from django.contrib import admin
from .models import Client, Invoice, InvoiceItem




@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'client', 'status', 'issued_date', 'due_date', 'total_amount']
    list_filter = ['status', 'issued_date']
    search_fields = ['client__name', 'client__email']
    readonly_fields = ['invoice_number']

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'name', 'quantity', 'unit_price', 'total_price']
