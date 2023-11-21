from django.forms import ModelForm, models

from store.models import Product


from django import forms
from store.models import ProductType, ProductSpecification, Category,ProductImage,ProductSpecificationValue


class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['name', 'is_active']

class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = ProductSpecification
        fields = ['product_type', 'name']




# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'slug', 'parent']

#     def clean_name(self):
#         name = self.cleaned_data['name']
#         # Check if the name already exists and print a message
#         if Category.objects.filter(name=name).exists():
#             print("Category with this name already exists")
#         return name

#     def clean_slug(self):
#         slug = self.cleaned_data['slug']
#         # Check if the slug already exists and print a message
#         if Category.objects.filter(slug=slug).exists():
#             print("Category with this slug already exists")
#         return slug



from django.core.exceptions import ValidationError


from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent']










class ProductSpecificationValueForm(forms.ModelForm):
    class Meta:
        model = ProductSpecificationValue
        fields = ['product', 'specification', 'value']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'alt_text', 'is_feature']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'regular_price','discount_price','product_type',
            'description','slug','is_active','qty','size'
                  
                  ]
        

