# Generated by Django 2.2.3 on 2019-07-27 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190727_2237'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categoryaddonprice',
            unique_together={('category', 'addon')},
        ),
        migrations.AlterUniqueTogether(
            name='itemaddonprice',
            unique_together={('item', 'addon')},
        ),
        migrations.AlterUniqueTogether(
            name='itemsizeprice',
            unique_together={('item', 'size')},
        ),
    ]