# Generated by Django 2.1.10 on 2019-07-02 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_review_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Beer'),
        ),
    ]
