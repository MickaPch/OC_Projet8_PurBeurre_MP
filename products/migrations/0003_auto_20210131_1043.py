# Generated by Django 3.1.3 on 2021-01-31 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210125_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='stores',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='stores',
            name='city',
        ),
    ]