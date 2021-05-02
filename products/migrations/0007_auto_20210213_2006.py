# Generated by Django 3.1.3 on 2021-02-13 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_products_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersave',
            name='compared_product',
        ),
        migrations.AlterField(
            model_name='usersave',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products'),
        ),
    ]