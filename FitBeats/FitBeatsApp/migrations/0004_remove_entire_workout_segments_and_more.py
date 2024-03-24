# Generated by Django 5.0.2 on 2024-03-24 05:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitBeatsApp', '0003_remove_workout_segment_exercise_names_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entire_workout',
            name='segments',
        ),
        migrations.AddField(
            model_name='exercise',
            name='entire_workout',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='FitBeatsApp.entire_workout'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Workout_Segment',
        ),
    ]
