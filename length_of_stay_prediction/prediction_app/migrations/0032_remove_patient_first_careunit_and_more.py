# Generated by Django 4.2.16 on 2024-12-20 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0031_patient_first_careunit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='first_careunit',
        ),
        migrations.AddField(
            model_name='admission',
            name='first_careunit',
            field=models.CharField(choices=[('ICU', 'ICU'), ('NICU', 'NICU')], default='ICU', max_length=5),
            preserve_default=False,
        ),
    ]
