# Generated by Django 3.2.5 on 2021-09-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0009_postdatamodel_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdatamodel',
            name='response',
            field=models.CharField(max_length=10),
        ),
    ]
