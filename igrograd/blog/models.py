from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Status(models.TextChoices):
    DRAFT = 'OF', 'Черновик'
    PUBLISHED = 'ON', 'Опубликован'

class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Публикация',
        help_text='Заполните название публикации')
    slug = models.SlugField(
        max_length=250,
        verbose_name='Слаг',
        help_text='Заполните уникальный фрагмент URL-адреса',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Заполните текст публикации'
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=('-publish',))
        ]

    def __str__(self) -> str:
        return self.title
