# Generated by Django 4.2.3 on 2023-07-27 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakecake_site', '0002_ready_cakes'),
    ]

    operations = [
        migrations.AddField(
            model_name='ready_cakes',
            name='index_page',
            field=models.BooleanField(default=1, verbose_name='Показывать на главной странице'),
            preserve_default=False,
        ),
    ]
