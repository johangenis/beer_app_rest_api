# Generated by Django 2.1.10 on 2019-07-03 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190702_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='tags',
        ),
    ]
