from django.forms import ModelForm, models

from store.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title','regular_price','discount_price','qty', 'description']