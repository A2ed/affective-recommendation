# Generated by Django 2.1.2 on 2018-12-16 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0008_emotionscotchsimilarity_similarity'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='emotionscotchsimilarity',
            table='Similarity',
        ),
    ]
