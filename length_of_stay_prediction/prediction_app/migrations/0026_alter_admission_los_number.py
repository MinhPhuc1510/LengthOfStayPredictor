# Generated by Django 4.2.16 on 2024-12-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0025_alter_admission_hadm_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='los_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
