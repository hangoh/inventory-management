# Generated by Django 4.2.2 on 2023-07-07 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Material', '0012_remove_material_material_name_not_empty_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='materialquantity',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 1)), name='quantity_greater_gte_1'),
        ),
    ]
