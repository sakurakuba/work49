from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')

    class Meta:
        abstract = True


class Issue(BaseModel):
    summary = models.CharField(max_length=100, verbose_name='summary')
    description = models.TextField(max_length=800, null=True, blank=True, verbose_name='description', default='not specified')
    status = models.ForeignKey("issueTracker.Status", on_delete=models.PROTECT, related_name='statuses', verbose_name='status')
    type = models.ForeignKey("issueTracker.Type", on_delete=models.PROTECT, related_name='types',  verbose_name='type')


    def __str__(self):
        return f"{self.id}. {self.summary} - status: {self.status}, type: {self.type}"

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

