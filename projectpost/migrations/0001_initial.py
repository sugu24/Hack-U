# Generated by Django 3.2.5 on 2021-09-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('username', models.CharField(max_length=40)),
                ('postdate', models.DateField(auto_now_add=True)),
                ('content', models.CharField(max_length=200)),
            ],
        ),
    ]
