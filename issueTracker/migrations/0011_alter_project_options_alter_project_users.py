# Generated by Django 4.0.6 on 2022-08-17 13:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issueTracker', '0010_project_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('add_users_to_project', 'Add users to project')], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]