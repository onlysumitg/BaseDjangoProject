# Generated by Django 3.2.9 on 2021-11-30 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemconfig',
            name='config',
            field=models.CharField(choices=[('APP_NAME', 'APPLICATION NAME'), ('SITE_HEADER', 'ADMIN SITE HEADER'), ('SITE_TITLE', 'ADMIN SITE TITLE'), ('INDEX_TITLE', 'ADMIN SITE INDEX TITLE'), ('POWERED_BY', 'POWERED BY WEBSITE')], max_length=25, primary_key=True, serialize=False, verbose_name='Configuration Name'),
        ),
    ]