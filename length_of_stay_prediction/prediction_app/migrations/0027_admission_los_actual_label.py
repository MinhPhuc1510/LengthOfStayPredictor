# Generated by Django 4.2.16 on 2024-12-13 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0026_alter_admission_los_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='los_actual_label',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]