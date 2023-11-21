from django.urls import path
from .views import ProductListView
from . import views

app_name = 'store'



from django.contrib.auth.decorators import user_passes_test
decorated_product_list_view = user_passes_test(lambda u: u.is_staff)(ProductListView.as_view())

urlpatterns = [
    path('', views.product_all, name='store_home'),  
    path('<slug:slug>', views.product_detail, name='product_detail'),   
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'), 

    path('product-list/', decorated_product_list_view, name='product-list'),
    path('search/', views.search, name='search'),

    path('product-reviews/<slug:slug>', views.product_reviews, name='product-reviews'),
    path('read-product_reviews/<slug:slug>', views.read_product_reviews, name='read-product-reviews'),
    path('company_reviews/', views.company_reviews, name='company-reviews'),
    path('read-company_reviews/', views.read_company_reviews, name='read-company-reviews'),

     
]
