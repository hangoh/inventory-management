# Generated by Django 4.2.2 on 2023-06-22 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_rename_product_uuid_product_uuid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='uuid',
            new_name='product_uuid',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='uuid',
            new_name='store_uuid',
        ),
    ]