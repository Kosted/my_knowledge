import pdb

from django.contrib.auth.models import User, AbstractUser
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

    def get_count(self):
        return self.count


class RegularUser(User):
    last_update_tag_action = models.CharField(max_length=10, default="")
    last_update_tag_id = models.IntegerField(default=0)

    last_update_memory_action = models.CharField(max_length=10, default="")
    last_update_memory_id = models.IntegerField(default=0)

    # На вход принимается строка с действием и экзепляр тега
    # del, upd, create,
    def update_last_edited_tag(self, action, tag):
        self.last_update_tag_action = action
        self.last_update_tag_id = tag.id

    # На вход принимается строка с действием и экзепляр памяти
    # del, upd, create,
    def update_last_edited_tag(self, action, memory):
        self.last_update_memory_action = action
        self.last_update_memory_id = memory.id


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
        # pdb.set_trace()
        tags_text = []
        for tag in self.tags.all():
            tags_text.append(tag.tag_text)
        return {"memory_text" :self.memory_text, "tags_text":tags_text, "pub_date":self.pub_date, "priority":self.priority}
