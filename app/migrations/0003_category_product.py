# Generated by Django 2.2.4 on 2020-06-14 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_register_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=50)),
                ('p_price', models.CharField(max_length=50)),
                ('note', models.TextField(max_length=2000)),
                ('cmp_price', models.CharField(max_length=50, null=True)),
                ('image', models.FileField(null=True, upload_to='documents/', verbose_name='Upload Image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Register_Detail')),
            ],
        ),
    ]
