# Generated by Django 3.1.3 on 2020-11-19 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_forming_detail_month'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forming_detail',
            name='user_id',
        ),
    ]
