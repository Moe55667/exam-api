# Generated by Django 4.2.11 on 2024-07-27 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_correct_answer_questiondetail_correct_version_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questiondetail',
            old_name='correct_version',
            new_name='correct_answer',
        ),
        migrations.RenameField(
            model_name='questiondetail',
            old_name='status',
            new_name='reason',
        ),
    ]
