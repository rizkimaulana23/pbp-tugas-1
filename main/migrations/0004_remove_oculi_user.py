# Generated by Django 4.1 on 2023-09-25 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_oculi_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oculi',
            name='user',
        ),
    ]
