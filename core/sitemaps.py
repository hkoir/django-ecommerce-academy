from django.contrib.sitemaps import Sitemap
from orders.models import OrderItem
from store.models import Category, Product

   
class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all()


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Category.objects.all()

   