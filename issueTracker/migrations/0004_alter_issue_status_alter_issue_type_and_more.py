# Generated by Django 4.0.6 on 2022-07-15 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0003_alter_issue_status_alter_issue_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(choices=[('new', 'new'), ('in_progress', 'in progress'), ('done', 'done')], on_delete=django.db.models.deletion.PROTECT, related_name='statuses', to='issueTracker.status', verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='type',
            field=models.ForeignKey(choices=[('task', 'task'), ('bug', 'bug'), ('enhancement', 'enhancement')], on_delete=django.db.models.deletion.PROTECT, related_name='types', to='issueTracker.type', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('in_progress', 'in progress'), ('done', 'done')], max_length=50, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='type',
            name='type',
            field=models.CharField(choices=[('task', 'task'), ('bug', 'bug'), ('enhancement', 'enhancement')], max_length=50, verbose_name='type'),
        ),
    ]
