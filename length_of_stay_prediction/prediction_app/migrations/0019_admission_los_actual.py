# Generated by Django 4.2.16 on 2024-12-02 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0018_merge_20241201_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='los_actual',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]