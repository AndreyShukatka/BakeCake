# Generated by Django 4.2.3 on 2023-07-28 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakecake_site', '0003_ready_cakes_index_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitly_statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegramm_name', models.CharField(max_length=200, verbose_name='Наименование канала')),
                ('url', models.TextField(blank=True, null=True, verbose_name='Ссылка')),
                ('number_transitions', models.IntegerField(verbose_name='Количество переходов')),
            ],
        ),
    ]
