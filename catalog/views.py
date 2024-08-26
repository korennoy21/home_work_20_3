from django.shortcuts import render, get_object_or_404
from slugify import slugify
from .models import Product, Category, People, BlogPost
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView

class MyBaseFooter:
    """Класс для выноса переопределения функции, чтобы в футере была инфа динамически.
       Класс сам по себе ничего не делает, просто существует для наследования,
       чтобы переопределить этот метод у других классов."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_list'] = Product.objects.all()
        return context


class ContactsView(MyBaseFooter, CreateView):
    """Отображение странички контактов и
    формы сбора контактов от пользователя с последующим сохранением в БД."""
    model = People
    fields = ('name', 'phone_number', 'message')
    success_url = reverse_lazy('catalog:contacts')


class IndexView(MyBaseFooter, ListView):
    """Главная страница каталога."""
    model = Product
    template_name = 'catalog/index.html'


class ProductView(MyBaseFooter, DetailView):
    """Детальный просмотр одного товара."""
    model = Product


class CategoryView(MyBaseFooter, DetailView):
    """Просмотр одной категории со всеми товарами в ней, реализованно через класс MyBaseFooter."""
    model = Category


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Получаем товар из базы данных по его pk
    context = {'product': product}  # Передаем товар в контексте шаблона
    return render(request, 'catalog/product_detail.html', context)  # Рендерим шаблон и передаем контекст


class BlogListView(MyBaseFooter, ListView):
    """Отображение списка всех блоговых записей."""
    model = BlogPost
    template_name = 'catalog/blog_list.html'
    context_object_name = 'blog_posts'

    def get_queryset(self):
        """Возвращает опубликованные записи, отсортированные по дате создания."""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')




###