# Generated by Django 2.2.3 on 2019-08-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cims', '0004_remove_extendeduser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='customer',
            field=models.BinaryField(),
        ),
    ]
