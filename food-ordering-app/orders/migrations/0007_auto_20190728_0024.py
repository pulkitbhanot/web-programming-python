# Generated by Django 2.2.3 on 2019-07-28 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20190727_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderlineitem',
            old_name='addon',
            new_name='order',
        ),
    ]