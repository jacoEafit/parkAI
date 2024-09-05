# Generated by Django 4.2.16 on 2024-09-04 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('parkingadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('org_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('org_nombre', models.CharField(max_length=40)),
                ('org_direccion', models.CharField(max_length=255)),
                ('org_telefono', models.CharField(max_length=20)),
                ('org_logo', models.ImageField(upload_to='logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('zna_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='vhc_carnet_id',
        ),
        migrations.AddField(
            model_name='parqueadero',
            name='prq_precio_dia',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='parqueadero',
            name='prq_precio_hora',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='vhc_usuario_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='celda',
            name='cld_conjunto_celdas_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.conjunto_celdas'),
        ),
        migrations.AlterField(
            model_name='egreso',
            name='egr_vehiculo_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.vehiculo'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fac_egreso_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.egreso'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fac_ingreso_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.ingreso'),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='ing_vehiculo_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.vehiculo'),
        ),
        migrations.AlterField(
            model_name='parqueadero',
            name='prq_nombre',
            field=models.CharField(max_length=40),
        ),
        migrations.DeleteModel(
            name='Carnet',
        ),
        migrations.AddField(
            model_name='zona',
            name='zna_parqueadero_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.parqueadero'),
        ),
        migrations.AddField(
            model_name='parqueadero',
            name='prq_universidad_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.organizacion'),
        ),
        migrations.AlterField(
            model_name='conjunto_celdas',
            name='cnj_parqueadero_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='parkingadmin.zona'),
        ),
    ]