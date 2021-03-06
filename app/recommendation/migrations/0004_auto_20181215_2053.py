# Generated by Django 2.1.2 on 2018-12-15 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0003_auto_20181115_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scotch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=100)),
                ('age', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='emotionset',
            old_name='master_emotion',
            new_name='parent_emotion',
        ),
    ]
