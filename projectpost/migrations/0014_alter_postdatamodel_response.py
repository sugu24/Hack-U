# Generated by Django 3.2.5 on 2021-09-04 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0013_alter_postdatamodel_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdatamodel',
            name='response',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='projectpost.postdatamodel'),
        ),
    ]
