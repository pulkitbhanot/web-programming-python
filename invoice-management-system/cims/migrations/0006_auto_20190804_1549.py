# Generated by Django 2.2.3 on 2019-08-04 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cims', '0005_auto_20190804_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='customer',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='supplier',
            field=models.BooleanField(),
        ),
    ]