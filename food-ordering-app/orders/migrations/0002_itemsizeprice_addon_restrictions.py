# Generated by Django 2.2.3 on 2019-07-27 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemsizeprice',
            name='addon_restrictions',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
