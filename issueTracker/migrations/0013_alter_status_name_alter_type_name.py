# Generated by Django 4.0.6 on 2022-07-15 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0012_alter_issue_status_alter_issue_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=50, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=50, verbose_name='type'),
        ),
    ]
