from django.urls import path
from . import views
from. views import checkout

app_name = 'payment'



urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripe_webhook),

    path('checkout/', checkout.as_view(), name='checkout'),
    path('confirm-address/', views.confirm_address, name='confirm_address'),
    path('process-order/', views.process_order, name='process_order'),
   
]
