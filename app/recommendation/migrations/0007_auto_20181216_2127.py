# Generated by Django 2.1.2 on 2018-12-16 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0006_auto_20181216_0005'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmotionSet',
            new_name='EmotionSyn',
        ),
    ]
