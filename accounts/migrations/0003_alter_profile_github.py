# Generated by Django 4.0.6 on 2022-08-19 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_github'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github',
            field=models.URLField(blank=True, null=True, verbose_name='GitHub'),
        ),
    ]
