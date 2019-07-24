from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
from django.utils import timezone


class Tag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    tag_text = models.CharField(max_length=20)
    count = models.IntegerField(default=0)

    # memory = models.ManyToManyField(Memory)

    def __str__(self):
        return self.tag_text

    def inc_count(self):
        self.count += 1


class Memory(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    memory_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    tags = models.ManyToManyField(Tag)
    priority = models.IntegerField(
        default=8,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])

    def __str__(self):
        return self.memory_text

    def field_to_list(self):
        return [self.memory_text,self.tags.all(),self.pub_date,self.priority]
