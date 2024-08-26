from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
from catalog import views
from catalog.apps import CatalogConfig
from .views import IndexView, ContactView

app_name = CatalogConfig.name

urlpatterns = [
                  path('blogs/', BlogListView.as_view(), name='blog_list'),
                  path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
                  path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),
                  path('blogs/<slug:slug>/update/', BlogUpdateView.as_view(), name='blog_update'),
                  path('blogs/<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
                  path('', IndexView.as_view(), name='index'),
                  path('contact/', ContactView.as_view(), name='contact'),
                  path('product/<int:pk>/', views.product_detail, name='product_detail')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
