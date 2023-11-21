from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'vendors'

urlpatterns = [
    # path('', views.vendors, name="vendors"),
    path('become-vendor/', views.become_vendor, name="become-vendor"),
    path('vendor-admin/', views.vendor_admin, name="vendor-admin"),
    path('edit-vendor/', views.edit_vendor, name="edit-vendor"),

    path('add-product-dashboard/', views.add_product_dashboard, name="add-product-dashboard"),
    
    path('add-product-step1/', views.add_product_step1, name="add-product-step1"),
    path('add-product-step2/<int:category_id>/', views.add_product_step2, name="add-product-step2"),  
    path('add-product-step3/<int:product_id>/', views.add_product_step3, name="add-product-step3"),
    path('add-product-step4/<int:product_id>/', views.add_product_step4, name="add-product-step4"),

    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name="login"),

    # path('<int:vendor_id>/', views.vendor, name="vendor"),
    
]

