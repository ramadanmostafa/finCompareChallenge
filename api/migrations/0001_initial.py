# Generated by Django 2.1.2 on 2018-10-24 16:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
