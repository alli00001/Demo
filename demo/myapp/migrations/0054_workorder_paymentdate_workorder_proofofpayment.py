# Generated by Django 4.2.8 on 2024-01-19 08:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0053_workorder_othercost'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='paymentDate',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='workorder',
            name='proofOfPayment',
            field=models.FileField(blank=True, null=True, upload_to='proof_of_payment/'),
        ),
    ]
