# Generated by Django 3.1.2 on 2020-11-24 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_product',
            new_name='total_products',
        ),
    ]