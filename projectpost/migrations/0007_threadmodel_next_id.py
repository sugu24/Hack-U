# Generated by Django 3.2.5 on 2021-09-03 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0006_auto_20210903_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadmodel',
            name='next_id',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
