# Generated by Django 4.2.8 on 2024-01-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0041_scopeofwork_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='pricing_type',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
