from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import string
from django.contrib.auth.models import User



class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-created_at']
           
    def __str__(self):
        return self.name
    
    


class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        SENT = 'SENT', _('Sent')
        PAID = 'PAID', _('Paid')
        OVERDUE = 'OVERDUE', _('Overdue')
        
    invoice_number = models.CharField(max_length=10, unique=True, blank=True)
    logo = models.ImageField(upload_to='invoices/', blank=True, null=True)
    business_name = models.CharField(max_length=50, null=True)
    business_website = models.URLField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    issued_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)
   
        
    def __str__(self):
        return f'Invoice {self.invoice_number}'
        
      
    def generate_invoice_number(self):
        prefix = "INV"
        while True:
            unique_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            invoice_number = f"{prefix}{unique_part}"
            if not Invoice.objects.filter(invoice_number=invoice_number).exists():
                return invoice_number
            
            
    class Meta:
        ordering = ['-created_at']
            
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['issued_date', 'due_date']),
        ]





class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name='quantity_positive',
            )
        ]
        
    def __str__(self):
        return f'{self.name} (x{self.quantity})'
    
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price
    