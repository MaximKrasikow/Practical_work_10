from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def posts():
    """Получение опубликованных постов из базы данных.
    Функция возвращает QuerySet с фильтрацией по:
    - полю is_published для постов и их категорий,
    - дате публикации (только те, что не позже текущей даты).
    """
    return Post.objects.select_related("category", "location", "author").filter(
        is_published=True,  # Только опубликованные посты
        category__is_published=True,  # Только опубликованными категориями
        pub_date__lte=datetime.now(),  # Посты с датой публикации до текущего времени
    )


def index(request):
    """Главная страница блога.
    Представление выводит пять последних постов, отсортированных
    по дате публикации. Результат отображается в шаблоне "index.html".
    """
    return render(request, "blog/index.html", {"post_list": posts()[:5]})


def post_detail(request, id):
    """Отображение полной информации о выбранной публикации.
    Используется get_object_or_404 для поиска поста по ID с фильтрацией
    по условиям функции posts(), чтобы отобразить только опубликованные записи.
    """
    post = get_object_or_404(posts(), id=id)
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    """Отображение всех публикаций внутри выбранной категории.
    Получение категории по слагу и фильтрация опубликованных постов, относящихся к ней.
    """
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    context = {"category": category, "post_list": posts().filter(category=category)}
    return render(request, "blog/category.html", context)
