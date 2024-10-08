# Generated by Django 4.2.16 on 2024-10-08 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingadmin', '0003_egreso_egr_imagen_vehiculo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conjunto_celdas',
            old_name='cnj_parqueadero_id',
            new_name='cnj_zona_id',
        ),
        migrations.RenameField(
            model_name='parqueadero',
            old_name='prq_universidad_id',
            new_name='prq_organizacion_id',
        ),
        migrations.AddField(
            model_name='conjunto_celdas',
            name='cnj_nombre_conjunto',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='parqueadero',
            name='prq_direccion_parqueadero',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='zona',
            name='zna_nombre_zona',
            field=models.CharField(default='', max_length=100),
        ),
    ]
