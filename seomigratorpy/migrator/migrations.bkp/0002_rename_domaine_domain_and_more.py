# Generated by Django 4.2.7 on 2023-11-27 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('migrator', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Domaine',
            new_name='Domain',
        ),
        migrations.RenameField(
            model_name='url_meta',
            old_name='Domaine_id',
            new_name='Domain_id',
        ),
    ]
