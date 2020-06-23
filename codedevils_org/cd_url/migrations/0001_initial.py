# Generated by Django 3.0.5 on 2020-06-23 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='Name', max_length=50)),
                ('url', models.URLField(db_column='Url')),
                ('slug', models.SlugField(db_column='Slug', help_text='The string used to reference the URL from within a Django template. The slug can only contain letters, numbers, underscores and hyphens.', max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Custom URL',
                'verbose_name_plural': 'Custom URLs',
                'db_table': 'custom_url',
                'ordering': ['name'],
                'managed': True,
            },
        ),
    ]
