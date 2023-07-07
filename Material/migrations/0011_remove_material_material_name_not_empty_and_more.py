# Generated by Django 4.2.2 on 2023-07-03 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Material', '0010_alter_material_price'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='material',
            name='material_name_not_empty',
        ),
        migrations.AddConstraint(
            model_name='material',
            constraint=models.CheckConstraint(check=models.Q(('name__exact', ''), _negated=True), name='material_name_not_empty'),
        ),
    ]