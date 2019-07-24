# Generated by Django 2.2.2 on 2019-07-11 12:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='memory',
        ),
        migrations.AddField(
            model_name='memory',
            name='autor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memory',
            name='priority',
            field=models.IntegerField(default=8, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='memory',
            name='tags',
            field=models.ManyToManyField(to='knowledge.Tag'),
        ),
    ]
