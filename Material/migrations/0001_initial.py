# Generated by Django 4.2.2 on 2023-06-08 10:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('material_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('name', models.CharField(max_length=256, unique=True, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.AutoField(primary_key=True, serialize=False)),
                ('store_name', models.CharField(max_length=256, unique=True, validators=[django.core.validators.MinLengthValidator(1)])),
                ('products', models.ManyToManyField(to='Material.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Material_Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('max_capacity', models.PositiveIntegerField()),
                ('current_capacity', models.PositiveIntegerField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.material')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.store')),
            ],
        ),
        migrations.CreateModel(
            name='Material_Quantity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Material.product')),
            ],
        ),
    ]
