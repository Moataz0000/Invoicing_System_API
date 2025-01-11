from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Invoice, InvoiceItem
from django.db.models import Sum, F


@receiver([post_save, post_delete], sender=InvoiceItem)
def update_invoice_total(sender, instance, **kwargs):
    invoice = instance.invoice
    total = invoice.items.aggregate(total=Sum(F('quantity') * F('unit_price')))['total'] or 0
    invoice.total_amount = total
    invoice.save()