# Generated by Django 2.2.3 on 2019-08-06 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cims', '0010_auto_20190806_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoiceState',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cims.InvoiceState'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicelineitem',
            name='invoiceLineItemStatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cims.InvoiceState'),
        ),
    ]