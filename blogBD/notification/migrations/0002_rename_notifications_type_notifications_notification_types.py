# Generated by Django 4.0.5 on 2022-07-06 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='notifications_type',
            new_name='notification_types',
        ),
    ]