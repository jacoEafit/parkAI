# Generated by Django 5.1.2 on 2024-10-10 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingadmin', '0005_remove_organizacion_org_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celda',
            name='cld_numero_celda',
        ),
        migrations.AddField(
            model_name='celda',
            name='cld_nombre_celda',
            field=models.CharField(default='', max_length=40),
        ),
    ]
