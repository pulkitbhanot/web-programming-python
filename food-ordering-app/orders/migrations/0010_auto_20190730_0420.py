# Generated by Django 2.2.3 on 2019-07-30 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20190730_0405'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemCount', models.IntegerField()),
                ('orderAmount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('orderTime', models.DateTimeField()),
                ('orderState', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderstates', to='orders.OrderState')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrderLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemCount', models.IntegerField()),
                ('perItemPrice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('topping_cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('itemName', models.CharField(max_length=64)),
                ('categoryName', models.CharField(max_length=64)),
                ('itemSizeName', models.CharField(max_length=64)),
                ('topping_list', models.CharField(max_length=500)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='orders.CustomerOrder')),
            ],
        ),
        migrations.RemoveField(
            model_name='orderlineitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderLineItem',
        ),
    ]