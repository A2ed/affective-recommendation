# Generated by Django 2.1.2 on 2018-12-16 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0005_auto_20181215_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scotch',
            name='idx',
        ),
        migrations.AlterModelTable(
            name='scotch',
            table='Scotch',
        ),
    ]
