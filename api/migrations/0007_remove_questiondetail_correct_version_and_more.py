# Generated by Django 4.2.11 on 2024-07-04 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_delete_studentmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questiondetail',
            name='correct_version',
        ),
        migrations.RemoveField(
            model_name='questiondetail',
            name='status',
        ),
        migrations.AddField(
            model_name='questiondetail',
            name='correct_answer',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='questiondetail',
            name='reason',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='questiondetail',
            name='section',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentreview',
            name='correct_answers',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentreview',
            name='correct_answers_total_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentreview',
            name='incorrect_answers_total_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentreview',
            name='total_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentreview',
            name='total_questions',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='studentreview',
            name='book_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studentreview',
            name='final_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='studentreview',
            name='incorrect_answers_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='studentreview',
            name='student_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
