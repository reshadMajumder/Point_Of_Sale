# Generated by Django 5.0.6 on 2024-08-05 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_bill_total_due_bill_total_paid_bill_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='user',
        ),
    ]
