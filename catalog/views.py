from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView,
    DetailView, DeleteView,
    UpdateView
)
from parso.utils import Version

from catalog.forms import VersionForm, CategoryForm, ProductForm
from catalog.models import (
    Product, Category,
    People, Version
)


# Create your views here.


class MyBaseFooter:
    """Класс для выноса переопределения функции чтобы в футере была инфа динамически
       не придумал как по другому это сделать класс сам по себе ничего не делает
       просто существует для наследования чтобы пере-определить этот метод у других классов"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_list'] = Product.objects.all()
        return context


class ContactsView(MyBaseFooter, CreateView):
    """Отображение странички контактов и
    формы сбора контактов от пользователя с последующим сохранением в бд"""
    model = People
    fields = ('name', 'phone_number', 'message')
    success_url = reverse_lazy('catalog:contacts')


class IndexView(MyBaseFooter, ListView):
    """Главная каталога"""
    model = Product
    template_name = 'catalog/index.html'


class ProductCreateView(MyBaseFooter, CreateView):
    """Страничка создания новой версии продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/product_form.html'


class ProductDeleteView(MyBaseFooter, DeleteView):
    """Страничка удаления версии продукта"""
    model = Product
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'


def get_success_url(self):
    return reverse('index')


class ProductDetailView(MyBaseFooter, DetailView):
    """Отображение одного продукта"""
    model = Product

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product.views += 1
        product.save()
        return context


class ProductUpdateView(MyBaseFooter, UpdateView):
    """Страничка редактирования продукта"""
    model = Product
    form_class = ProductForm  # Укажите форму создания/редактирования продукта в форме ProductForm
    fields = ['name', 'description', 'price', 'image']  # Укажите все поля, которые должны быть в форме
    success_url = reverse_lazy('catalog:index')  # Обновите URL на страницу индекса
    template_name = 'catalog/product_form.html'


    def get_success_url(self):
        # Используйте правильное имя для URL-шаблона
        return reverse('product_detail', kwargs={'pk': self.object.pk})



class CategoryDetailView(MyBaseFooter, DetailView):
    """Одна категория со всеми товарами в ней реализованно через класс MyBaseFooter"""
    model = Category



class AerfonView(MyBaseFooter, ListView):
    """Страничка с акционными товарами"""
    template_name = 'catalog/aerfon.html'

    def get_queryset(self):
        return Product.objects.filter(is_aerfon=True)

class CategoryCreateView(MyBaseFooter, CreateView):
    """Страничка создания новой категории"""
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'


class CategoryUpdateView(MyBaseFooter, UpdateView):
    """Страничка редактирования категории"""
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'pk': self.object.pk})

class CategoryDeleteView(MyBaseFooter, DeleteView):
    """Страничка удаления категории"""
    model = Category
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'

    def get_success_url(self):
        return reverse('catalog:index')


class VersionCreateView(MyBaseFooter, CreateView):
    """Страничка создания новой версии продукта"""
    model = Version
    form_class = VersionForm
    fields = ['product', 'code', 'version']
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'


class VersionUpdateView(MyBaseFooter,Version, UpdateView):
    """Страничка редактирования версии продукта"""
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('version_detail', kwargs={'pk': self.object.pk})

class VersionDeleteView(MyBaseFooter, DeleteView):
     """Страничка удаления версии продукта"""
     model = Version
     success_url = reverse_lazy('catalog:index')
     template_name = 'catalog/object_confirm_delete.html'



