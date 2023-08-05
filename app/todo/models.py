import uuid

from django.db import models
from django.utils import timezone


class TodoQuerySet(models.QuerySet):
    def filter_status_new(self, *args, **kwargs):
        return self.filter(status=Todo.Todo_Status.NEW, *args, **kwargs)

    def filter_status_wip(self, *args, **kwargs):
        return self.filter(status=Todo.Todo_Status.WIP, *args, **kwargs)

    def filter_status_done(self, *args, **kwargs):
        return self.filter(status=Todo.Todo_Status.DONE, *args, **kwargs)


class Todo(models.Model):
    class Todo_Status(models.TextChoices):
        NEW = "new", "未着手"
        WIP = "wip", "着手中"
        DONE = "done", "完了"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=Todo_Status.choices,
        default=Todo_Status.NEW,
    )
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TodoQuerySet.as_manager()

    def is_new(self):
        return self.status == self.Todo_Status.NEW

    def is_wip(self):
        return self.status == self.Todo_Status.WIP

    def is_done(self):
        return self.status == self.Todo_Status.DONE

    def is_deadline_exceeded(self):
        return self.deadline and self.deadline < timezone.now()

    def caluculate_remaining_date(self) -> int:
        if self.deadline:
            return (self.deadline - timezone.now()).days
        return 0
