# Generated by Django 3.2.7 on 2021-09-19 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wars', '0002_auto_20210919_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='battle_number',
            field=models.PositiveIntegerField(db_index=True, null=True, unique=True),
        ),
    ]
