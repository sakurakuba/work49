from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.datetime_safe import date


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')

    class Meta:
        abstract = True


class Issue(BaseModel):
    summary = models.CharField(max_length=100, verbose_name='summary')
    description = models.TextField(max_length=800, null=True, blank=True, verbose_name='description', default='not specified')
    status = models.ForeignKey("issueTracker.Status", on_delete=models.PROTECT, related_name='statuses', verbose_name='status')
    type = models.ManyToManyField("issueTracker.Type",  related_name='types')
    project = models.ForeignKey("issueTracker.Project", on_delete=models.CASCADE, related_name='projects', verbose_name='project')

    def __str__(self):
        return f"{self.id}. {self.summary} - status: {self.status}, type: {self.type.all()}"

    def get_absolute_url(self):
        return reverse('issue_view', kwargs={"pk": self.pk})

    class Meta:
        db_table = 'issues'
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='status', default="new")

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='type', default="task")

    def __str__(self):
        return self.name


class Project(models.Model):
    start_date = models.DateField(default=date.today, verbose_name='Start date')
    end_date = models.DateField(blank=True, default='', verbose_name='End date')
    project_name = models.CharField(max_length=50, verbose_name='Project name')
    project_description = models.TextField(max_length=1000, verbose_name='Project description', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')

    def __str__(self):
        return f"{self.id}. {self.project_name} - start date: {self.start_date}, end date: {self.end_date}"

    def get_absolute_url(self):
        return reverse('project_view', kwargs={"pk": self.pk})

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

