# Generated by Django 2.2.3 on 2019-08-04 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cims', '0006_auto_20190804_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='supplier',
            field=models.BooleanField(default=False),
        ),
    ]
