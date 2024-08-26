from django.shortcuts import render, get_object_or_404
from slugify import slugify

from .models import Product
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from django.views.generic import TemplateView

# Пример CBV
class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'

class ContactView(TemplateView):
    template_name = 'catalog/contact.html'


class BlogListView(ListView):
    model = BlogPost
    template_name = 'catalog/blog_list.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blog_detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'catalog/blog_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title)
        self.object.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'catalog/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blog_detail', args=[self.object.slug])


class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')




def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Получаем товар из базы данных по его pk
    context = {'product': product}  # Передаем товар в контексте шаблона
    return render(request, 'catalog/product_detail.html', context)  # Рендерим шаблон и передаем контекст
