from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    IndexView, ContactsView, ProductDetailView,
    CategoryDetailView, ProductUpdateView, ProductDeleteView,
    ProductCreateView, CategoryDeleteView,AerfonView
)

app_name = CatalogConfig.name

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
                  path('product/create/', ProductCreateView.as_view(), name='product_create'),

                  path('contacts/', ContactsView.as_view(), name='contacts'),
                  path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
                  path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

                  path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
                  path('category/update/<int:pk>/', ProductUpdateView.as_view(), name='category_update'),
                  path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
                  path('category/create/', ProductCreateView.as_view(), name='category_create'),
                  path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_info'),
                  path('aerfon/', AerfonView.as_view(), name='aerfon')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
