import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProductSitemap,CategorySitemap

sitemaps = {
   
    'model2': ProductSitemap,
    'model3': CategorySitemap,
   
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls", namespace="account")),
    path("vendors/", include("vendors.urls", namespace="vendors")),
   
    path("", include("store.urls", namespace="store")),
    path("basket/", include("basket.urls", namespace="basket")),
    path("payment/", include("payment.urls", namespace="payment")),
  
    path("orders/", include("orders.urls", namespace="orders")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("seller/", include("seller.urls", namespace="seller")),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("companyprofile/", include("companyprofile.urls", namespace="companyprofile")),
     path("visitors/", include("visitors.urls", namespace="visitors")),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
