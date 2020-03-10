# Generated by Django 3.0.3 on 2020-03-02 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0008_regularuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regularuser',
            name='last_update_memory_action',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='regularuser',
            name='last_update_memory_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='regularuser',
            name='last_update_tag_action',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='regularuser',
            name='last_update_tag_id',
            field=models.IntegerField(default=0),
        ),
    ]