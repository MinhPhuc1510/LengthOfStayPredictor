# Generated by Django 4.2.16 on 2024-11-24 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0013_admission_created_time_admission_updated_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prediction_app.room'),
        ),
    ]
