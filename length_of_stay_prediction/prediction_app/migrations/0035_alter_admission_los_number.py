# Generated by Django 4.2.16 on 2024-12-21 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0034_alter_admission_diagnose_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='los_number',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
    ]
