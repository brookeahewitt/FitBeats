# Generated by Django 5.0.2 on 2024-03-24 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitBeatsApp', '0004_remove_entire_workout_segments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entire_workout',
            name='playlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FitBeatsApp.playlist'),
        ),
    ]