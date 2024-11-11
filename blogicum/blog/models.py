from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
TEXT_LENGTH = 256  # Ограничение на длину текстовых полей


class BaseModel(models.Model):
    """Абстрактная модель, включающая общие поля.
    Поля:
    - is_published: флаг, определяющий видимость записи на сайте.
    - created_at: дата добавления записи.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    class Meta:
        abstract = True  # Определяет модель как абстрактную


class Category(BaseModel):
    """Модель категории постов блога.
    Поля:
    - title: название категории.
    - description: текстовое описание категории.
    - slug: уникальный идентификатор для URL.
    """

    title = models.CharField(max_length=TEXT_LENGTH, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text="Идентификатор страницы для URL; разрешены символы "
        "латиницы, цифры, дефис и подчёркивание.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(BaseModel):
    """Модель местоположения, связанная с постами.
    Поля:
    - name: название места.
    """

    name = models.CharField(max_length=TEXT_LENGTH, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(BaseModel):
    """Модель публикации (поста) в блоге.
    Поля:
    - title: заголовок поста.
    - text: текст поста.
    - pub_date: дата и время публикации (позволяет отложенную публикацию).
    - author: ссылка на автора (пользователя).
    - location: местоположение, связанное с публикацией.
    - category: категория поста.
    """

    title = models.CharField(max_length=TEXT_LENGTH, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
        "можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",  # Установка обратной связи с постами пользователя
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Местоположение",
        related_name="posts",  # Установка обратной связи с постами местоположения
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="posts",  # Установка обратной связи с постами категории
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]  # Сортировка по дате публикации, последние сначала
