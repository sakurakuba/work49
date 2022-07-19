# Generated by Django 4.0.6 on 2022-07-18 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0003_rename_type_issue_type_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='type_old',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='types_old', to='issueTracker.type', verbose_name='type'),
        ),
    ]