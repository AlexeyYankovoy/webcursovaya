# Generated by Django 5.0 on 2023-12-22 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_orderstatus_color_alter_orderitem_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.SET_DEFAULT, to='app.orderstatus', verbose_name='Статус'),
        ),
    ]
