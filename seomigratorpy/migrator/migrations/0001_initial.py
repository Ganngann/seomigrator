# Generated by Django 4.2.7 on 2023-11-27 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domaine',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Subdomain',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Url_meta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('http_status', models.IntegerField()),
                ('Domaine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.domaine')),
                ('Page_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.page')),
                ('Subdomain_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.subdomain')),
                ('url_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.url')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='url_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.url'),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('queryParam', models.CharField(max_length=255)),
                ('protocol', models.CharField(max_length=255)),
                ('fragment', models.CharField(max_length=255)),
                ('page_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.page')),
                ('url_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='migrator.url')),
            ],
        ),
    ]
