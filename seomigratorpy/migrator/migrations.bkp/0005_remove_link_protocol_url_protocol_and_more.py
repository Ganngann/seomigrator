# Generated by Django 4.2.7 on 2023-11-28 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migrator', '0004_url_domain_id_url_page_id_url_subdomain_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='protocol',
        ),
        migrations.AddField(
            model_name='url',
            name='protocol',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='http_status',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='path',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
