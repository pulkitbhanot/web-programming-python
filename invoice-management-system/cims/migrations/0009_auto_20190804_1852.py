# Generated by Django 2.2.3 on 2019-08-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cims', '0008_auto_20190804_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='lastLoginTime',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
