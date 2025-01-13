from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    export_invoice,
    ClientViewset,
    InvocieViewSet,
    InvoiceItemViewSet,
    # RegisterView
)


app_name = 'invoices'


router = DefaultRouter()
router.register(r'clients', ClientViewset, basename='clients')
router.register(r'invoices', InvocieViewSet, basename='invoices')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoice-item')



urlpatterns = [
    path('invoice/<int:invoice_id>/export/<str:format>/', export_invoice, name='export_invoice'),
    # path('register/', RegisterView.as_view(), name='register'),

    # ViewSets
    path('', include(router.urls))
]
