"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import ProductsByCategoryView

app_name = 'catalog'

urlpatterns = [
    path('list/', views.ProductListView.as_view(), name='product_list'),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("product/create", views.ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", views.ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", views.ProductDeleteView.as_view(), name="product_delete"),
    path("product/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/unpublish", views.ProductUnpublishView.as_view(), name="product_unpublish"),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
]
