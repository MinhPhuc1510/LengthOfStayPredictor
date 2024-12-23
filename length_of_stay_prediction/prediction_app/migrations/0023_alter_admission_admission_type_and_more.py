# Generated by Django 4.2.16 on 2024-12-08 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0022_alter_admission_hadm_id_alter_patient_ethnicity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='admission_type',
            field=models.CharField(choices=[('EMERGENCY', 'EMERGENCY'), ('ELECTIVE', 'ELECTIVE'), ('URGENT', 'URGENT')], max_length=10),
        ),
        migrations.AlterField(
            model_name='admission',
            name='clinical_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='admission',
            name='los_lable',
            field=models.CharField(blank=True, choices=[('Less than 3 days', 'Less than 3 days'), ('3-7 days', '3-7 days'), ('7-14 days', '7-14 days'), ('More than 14 days', 'More than 14 days')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='admission',
            name='status',
            field=models.CharField(blank=True, choices=[('In Treatment', 'In Treatment'), ('Dischagred', 'Dischagred')], default='In Treatment', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='patient',
            name='religion',
            field=models.CharField(choices=[('CATHOLIC', 'CATHOLIC'), ('PROTESTANT QUAKER', 'PROTESTANT QUAKER'), ('UNOBTAINABLE', 'UNOBTAINABLE'), ('JEWISH', 'JEWISH'), ('NOT SPECIFIED', 'NOT SPECIFIED'), ('OTHER', 'OTHER')], max_length=20),
        ),
    ]
