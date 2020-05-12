from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Model to store the address for supplier/customer in the system
class Address(models.Model):
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=5)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.address1}  - {self.address2} - {self.zipcode} - {self.state}  - {self.country}"


# Referenced https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html to look at how to extend existing DJango models
class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supplier = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)
    businessName = models.CharField(max_length=200)
    lastLoginTime = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.user.id} - {self.supplier} - {self.customer}  - {self.businessName}"


# When a user is created, automatically create a record in the extended user table as well
@receiver(post_save, sender=User)
def create_extended_user(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_extended_user(sender, instance, **kwargs):
    instance.extendeduser.save()


# Model to represent linked suppliers customers in the system
class SupplierCustomerRelation(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suppliercustomer")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customersupplier")

    class Meta:
        unique_together = (("supplier", "customer"),)

    def __str__(self):
        return f"{self.id} - {self.supplier.id} - {self.customer.id}"


# Model for storing Invoice state
class InvoiceState(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} - {self.name}"


# Model for storing Invoice details
class Invoice(models.Model):
    description = models.CharField(max_length=500)
    createdTime = models.DateTimeField()
    lastUpdatedTime = models.DateTimeField()
    invoiceDueDate = models.DateField()
    invoiceState = models.ForeignKey(InvoiceState, on_delete=models.CASCADE)
    invoiceItemCount = models.IntegerField()
    invoiceAmount = models.DecimalField(max_digits=5, decimal_places=2)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supplier")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return f"{self.id} - {self.description} - {self.createdTime}  - {self.supplier.id}  - {self.customer.id}"


# Model for storing different notes on the invoice
class InvoiceNote(models.Model):
    description = models.CharField(max_length=500)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    createdTime = models.DateTimeField()

    def __str__(self):
        return f"{self.id} - {self.description} - {self.invoice.id}"


# Model for storing invoice line items that were a part of the invoice
class InvoiceLineItem(models.Model):
    lineItemPrice = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=500)
    invoiceLineItemStatus = models.ForeignKey(InvoiceState, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/', default=None)

    def __str__(self):
        return f"{self.id} - {self.description} - {self.invoiceLineItemStatus.name} - {self.lineItemPrice}"


# Model for storing different notes on the invoice item level
class InvoiceLineItemNote(models.Model):
    description = models.CharField(max_length=500)
    invoiceLineItem = models.ForeignKey(InvoiceLineItem, on_delete=models.CASCADE)
    createdTime = models.DateTimeField()

    def __str__(self):
        return f"{self.id} - {self.description} - {self.invoiceLineItem.id}"
