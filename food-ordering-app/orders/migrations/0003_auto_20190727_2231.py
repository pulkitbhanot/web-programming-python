# Generated by Django 2.2.3 on 2019-07-27 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_itemsizeprice_addon_restrictions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderState',
        ),
        migrations.DeleteModel(
            name='OrderLineItem',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
