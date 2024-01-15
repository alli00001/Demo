# Generated by Django 4.2.8 on 2024-01-01 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_remove_workorder_attachment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='deductions',
            field=models.ManyToManyField(blank=True, to='myapp.deduction'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='workOrder',
            field=models.ManyToManyField(blank=True, to='myapp.scopeofwork'),
        ),
    ]
