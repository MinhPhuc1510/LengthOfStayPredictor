# Generated by Django 4.2.16 on 2024-11-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0011_remove_admission_room_patient_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
