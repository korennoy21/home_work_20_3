from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView,
    DetailView, DeleteView,
    UpdateView,
)
from parso.utils import Version
from transformers import pipeline

from catalog.forms import VersionForm, CategoryForm, ProductForm
from catalog.models import (
    Product, Category,
    People, Version
)


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('user:login')
    redirect_field_name ='redirect_to'
    raise_exception = True



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
    form_class = ProductForm  # Исправлено: использована форма ProductForm
    success_url = reverse_lazy('catalog:contacts')
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('catalog:index')  # Исправлено: указан правильный URL-паттерн


class ProductUpdateView(MyBaseFooter, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Allow editing if user is the owner or has the 'change_product' permission (moderator)
        if request.user != product.owner and not request.user.has_perm('catalog.change_product'):
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.get_object().owner
        context['can_edit'] = self.request.user.has_perm('catalog.change_product')
        return context

class IndexView(MyBaseFooter, ListView):
    
    """Главная каталога"""
    model = Product
    template_name = 'catalog/index.html'


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Получаем все продукты
    products = context['products']

    # Для каждого продукта находим активную версию
    product_versions = {}
    for product in products:
        active_version = Version.objects.filter(product=product, is_active=True).first()
        product_versions[product.id] = active_version

    # Передаем активные версии в контекст
    context['product_versions'] = product_versions
    return context

class ProductCreateView(LoginRequiredMixin,MyBaseFooter, CreateView):
    """Страничка создания нового продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'


    def get_success_url(self):
        return reverse('catalog:detail', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductDeleteView(MyBaseFooter, DeleteView):
    """Страничка удаления продукта"""
    model = Product
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'


def get_success_url(self):
    return reverse('index')



class ProductDetailView(DetailView):
    """Страничка деталей продукта"""
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['version'] = Version.objects.filter(product=product, is_active=True).first()
        return context

class ProductUpdateView(MyBaseFooter, UpdateView):
    """Страничка редактирования продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:detail')
    template_name = 'catalog/object_form.html'

    def get_success_url(self):
        return reverse('catalog:detail', args=[self.object.pk])


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
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_form.html'


class VersionUpdateView(MyBaseFooter, UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:detail')
    template_name = 'catalog/object_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        version = self.get_object()
        context['product'] = version.product  # Добавляем продукт в контекст
        return context

    def get_success_url(self):
        return reverse('catalog:detail', kwargs={'pk': self.object.product.pk})


class VersionDeleteView(MyBaseFooter, DeleteView):
    """Страничка удаления версии продукта"""
    model = Version
    success_url = reverse_lazy('catalog:index')
    template_name = 'catalog/object_confirm_delete.html'