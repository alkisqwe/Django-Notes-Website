# Generated by Django 5.0.6 on 2024-06-03 03:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memos', '0003_note_notedate_note_notename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='notedate',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 3, 3, 25, 33, 373720)),
        ),
        migrations.AlterField(
            model_name='note',
            name='notename',
            field=models.CharField(default='unamed', max_length=100),
        ),
    ]
