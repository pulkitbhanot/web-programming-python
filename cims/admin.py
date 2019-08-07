from django.contrib import admin

from cims.models import Address, ExtendedUser, InvoiceState, Invoice, InvoiceNote, InvoiceLineItem, InvoiceLineItemNote, \
    SupplierCustomerRelation

# Register your models here.

admin.site.register(Address)
admin.site.register(ExtendedUser)
admin.site.register(InvoiceState)
admin.site.register(Invoice)
admin.site.register(InvoiceNote)
admin.site.register(InvoiceLineItem)
admin.site.register(InvoiceLineItemNote)
admin.site.register(SupplierCustomerRelation)
