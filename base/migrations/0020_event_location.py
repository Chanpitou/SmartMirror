# Generated by Django 5.0 on 2024-02-11 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_event_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.TextField(max_length=400, null=True),
        ),
    ]