# Generated by Django 2.1.10 on 2019-07-02 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190702_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
