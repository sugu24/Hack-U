# Generated by Django 3.2.5 on 2021-09-02 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpost', '0004_auto_20210902_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdatamodel',
            name='postdate',
            field=models.CharField(max_length=20),
        ),
    ]
