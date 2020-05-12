# Generated by Django 2.2.3 on 2019-08-07 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cims', '0014_invoicenote_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliercustomerrelation',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customersupplier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='suppliercustomerrelation',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliercustomer', to=settings.AUTH_USER_MODEL),
        ),
    ]
