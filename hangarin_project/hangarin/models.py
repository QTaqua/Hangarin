from django.contrib.auth.models import User
from django.db import models


# Common base model to avoid repeating timestamp fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Priority(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20, default="Pending"
    )  # Pending, Completed
    priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, related_name="tasks"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Note(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"


class SubTask(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    parent_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    class Meta:
        verbose_name = "Sub Task"
        verbose_name_plural = "Sub Tasks"

    def __str__(self):
        return self.title