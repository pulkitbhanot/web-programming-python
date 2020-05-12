# Generated by Django 2.2.3 on 2019-08-03 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=5)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('createdTime', models.DateTimeField()),
                ('lastUpdatedTime', models.DateTimeField()),
                ('invoiceDueDate', models.DateField()),
                ('invoiceItemCount', models.IntegerField()),
                ('invoiceAmount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lineItemPrice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cims.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceLineItemNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('invoiceLineItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cims.InvoiceLineItem')),
            ],
        ),
        migrations.AddField(
            model_name='invoicelineitem',
            name='invoiceLineItemStatus',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cims.InvoiceState'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoiceState',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cims.InvoiceState'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='supplier',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.BinaryField()),
                ('customer', models.BinaryField(blank=True)),
                ('businessName', models.CharField(max_length=200)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cims.Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
