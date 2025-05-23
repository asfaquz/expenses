# Generated by Django 5.2.1 on 2025-05-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraccount',
            options={'ordering': ['user_id'], 'verbose_name': 'User Account', 'verbose_name_plural': 'User Accounts'},
        ),
        migrations.RemoveIndex(
            model_name='useraccount',
            name='user_accoun_user_id_32ff6e_idx',
        ),
        migrations.RenameField(
            model_name='useraccount',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='password',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='username',
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(fields=['user_id'], name='user_accoun_user_id_c5dc4e_idx'),
        ),
    ]
