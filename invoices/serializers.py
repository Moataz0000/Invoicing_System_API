from django.urls import reverse
from rest_framework import serializers
from .models import Invoice, InvoiceItem, Client
import bleach
import re  
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        default_timezone=get_current_timezone(),
        read_only=True,
    )

    class Meta:
        model = Client
        fields = '__all__'

    def validate(self, attrs):
        """Clean all string fields"""
        for field in ['name', 'email', 'phone', 'address', 'postal_code']:
            if field in attrs and attrs[field]:  # Check if the field exists and is not None
                #  bleach to remove HTML tags
                cleaned_value = bleach.clean(
                    str(attrs[field]),
                    tags=[],  # Allow no tags
                    attributes={},  # Allow no attributes
                    strip=True  # Strip unwanted tags instead of escaping them
                )
                # remove JavaScript code or script-like patterns
                cleaned_value = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', cleaned_value, flags=re.IGNORECASE)
                cleaned_value = re.sub(r'on\w+=".*?"', '', cleaned_value, flags=re.IGNORECASE)  # Remove event handlers
                cleaned_value = re.sub(r'javascript:', '', cleaned_value, flags=re.IGNORECASE)  # Remove "javascript:"
                cleaned_value = re.sub(r'alert\(.*?\)', '', cleaned_value, flags=re.IGNORECASE)  # Remove "alert()"
                attrs[field] = cleaned_value.strip()  # Remove leading/trailing whitespace
        return attrs
    
    
    

class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField(source='get_client')
    pdf_link = serializers.SerializerMethodField()
    csv_link = serializers.SerializerMethodField()

    
    class Meta:
        model = Invoice
        fields =  [
            'id', 'invoice_number', 'business_name', 'business_website', 'client', 
            'status', 'issued_date', 'due_date', 'total_amount', 'created_at', 
            'pdf_link', 'csv_link',
        ]
        extra_kwargs = {
            'invoice_number': {'read_only': True},
            'total_amount': {'read_only': True},
        }
        
    
    def get_client(self, obj: Invoice):
        return obj.client.name if obj else None
    
    
    def get_pdf_link(self, obj):
        """Generate the PDF download link dynamically."""
        
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('invoices:export_invoice', kwargs={'invoice_id': obj.id, 'format': 'pdf'})
            )
        return None
    
    
    def get_csv_link(self, obj):
        """Generate the PDF download link dynamically."""
        
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('invoices:export_invoice', kwargs={'invoice_id': obj.id, 'format': 'csv'})
                )
        return None
    
    
    



class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        
        




# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password']
#         )
#         return user