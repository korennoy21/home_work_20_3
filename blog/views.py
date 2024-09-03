from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import BlogEntre
from catalog.views import MyBaseFooter


class BlogIndexView(ListView):
    model = BlogEntre
    template_name = 'blog/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=True)
        return queryset


class BlogDetailView(MyBaseFooter, DetailView):
    """Отображение одной записи блога"""
    model = BlogEntre
    template_name = 'blog/blogentry_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object


class BlogCreateView(CreateView, MyBaseFooter):
    model = BlogEntre
    fields = ['title', 'content']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView, MyBaseFooter):
    model = BlogEntre
    fields = ['title', 'content']
    success_url = reverse_lazy('blog:detail')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'slug': self.object.slug})


class BlogDeleteView(DeleteView, MyBaseFooter):
    model = BlogEntre
    success_url = reverse_lazy('blog:index')
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'