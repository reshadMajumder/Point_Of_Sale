# Generated by Django 5.0.6 on 2024-08-12 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_bill_total_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField()),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.supplier')),
            ],
        ),
    ]
