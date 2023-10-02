# Generated by Django 4.2.5 on 2023-10-02 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='status',
            new_name='is_verified',
        ),
        migrations.RemoveField(
            model_name='otp',
            name='username',
        ),
        migrations.AddField(
            model_name='otp',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
