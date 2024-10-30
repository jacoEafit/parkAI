# Generated by Django 5.1.2 on 2024-10-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingadmin', '0006_remove_celda_cld_numero_celda_celda_cld_nombre_celda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celda',
            name='cld_estado',
            field=models.CharField(choices=[('occupied', 'occupied'), ('empty', 'empty'), ('unavailable', 'unavailable')], default='unavailable', max_length=20),
        ),
    ]
