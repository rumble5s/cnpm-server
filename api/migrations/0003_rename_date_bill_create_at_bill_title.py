# Generated by Django 4.2.6 on 2023-12-18 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_register_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='date',
            new_name='create_at',
        ),
        migrations.AddField(
            model_name='bill',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
    ]
