from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Status.PUBLISHED)


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
        unique_for_date='publish',
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
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name='Статус')
    objects = models.Manager()
    published = PublishManager()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=('-publish',))
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug,
                           ]
                       )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
        help_text='Выберите публикацию для комментирования'
    )
    name = models.CharField(
        max_length=80,
        verbose_name='Имя',
        help_text='Укажите Ваше имя'
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите действующий адрес электронной почты'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Заполните текст комментария'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(
        default=True,
        verbose_name='Активирован',
        help_text='Если "Активирован" комментарий отображается на сайте'
    )

    class Meta:
        ordering = ('created',)
        indexes = [
            models.Index(fields=('created',))
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Комментарий от {self.name} на {self.post}'
