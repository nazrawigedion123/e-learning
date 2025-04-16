from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Progress, LessonProgress, ChapterProgress


@receiver(post_save, sender=LessonProgress)
def update_lesson_progress(sender, instance, created, **kwargs):
    """
    Update chapter progress when lesson progress changes
    """
    if instance.completed:
        # Get the chapter this lesson belongs to
        chapter = instance.lesson.chapter

        # Get or create chapter progress record
        chapter_progress, created = ChapterProgress.objects.get_or_create(
            progress=instance.progress,
            chapter=chapter
        )

        # Check if all lessons in this chapter are completed
        total_lessons = chapter.lessons.count()
        completed_lessons = LessonProgress.objects.filter(
            progress=instance.progress,
            lesson__chapter=chapter,
            completed=True
        ).count()

        # Update chapter completion status
        chapter_progress.completed = (completed_lessons >= total_lessons)
        if chapter_progress.completed:
            chapter_progress.completed_at = timezone.now()
        chapter_progress.save()

        # Update overall course progress status
        update_course_progress(instance.progress)


@receiver(pre_save, sender=ChapterProgress)
def update_chapter_progress(sender, instance, **kwargs):
    """
    Update course progress when chapter progress changes
    """
    if instance.pk:  # Only for updates, not creations
        old_instance = ChapterProgress.objects.get(pk=instance.pk)
        if instance.completed != old_instance.completed:
            update_course_progress(instance.progress)


def update_course_progress(progress):
    """
    Helper function to update course-level progress status
    """
    total_chapters = progress.course.chapters.count()
    completed_chapters = progress.completed_chapters.filter(
        chapterprogress__completed=True
    ).count()

    if completed_chapters >= total_chapters and total_chapters > 0:
        progress.status = Progress.Status.COMPLETED
    elif progress.completed_lessons.exists():
        progress.status = Progress.Status.IN_PROGRESS
    else:
        progress.status = Progress.Status.NOT_STARTED
    progress.save()