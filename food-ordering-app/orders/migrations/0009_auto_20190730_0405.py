# Generated by Django 2.2.3 on 2019-07-30 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20190730_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderid',
        ),
        migrations.AddField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]