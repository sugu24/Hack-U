# Generated by Django 3.2.5 on 2021-09-03 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0005_alter_postdatamodel_postdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdatamodel',
            name='bad',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='postdatamodel',
            name='good',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
