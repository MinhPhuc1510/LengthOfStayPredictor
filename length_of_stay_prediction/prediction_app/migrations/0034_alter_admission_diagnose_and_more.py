# Generated by Django 4.2.16 on 2024-12-20 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0033_remove_admission_icd_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='diagnose',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='admission',
            name='first_careunit',
            field=models.TextField(choices=[('ICU', 'ICU'), ('NICU', 'NICU')], max_length=4),
        ),
    ]
