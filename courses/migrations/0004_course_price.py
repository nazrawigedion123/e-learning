# Generated by Django 5.1.5 on 2025-02-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_question_course_users_chapter_lesson_progress_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
