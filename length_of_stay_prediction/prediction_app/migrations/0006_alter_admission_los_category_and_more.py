# Generated by Django 4.2.16 on 2024-11-24 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0005_remove_patient_clinical_note_admission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='los_category',
            field=models.CharField(choices=[('E', 'Emergency '), ('U', 'Urgent '), ('EL', 'Elective '), ('OT', 'Other')], default='I', max_length=2),
        ),
        migrations.AlterField(
            model_name='admission',
            name='los_number',
            field=models.IntegerField(default=0),
        ),
    ]
