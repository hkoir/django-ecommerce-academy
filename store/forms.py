from django import forms
from store.models import ProductReview
from .models import CompanyReview

from django import forms
from store.models import Product, ProductSpecification, Category, ProductType, ProductSpecificationValue, ProductImage, ProductVideo

from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, ProductSpecification, ProductSpecificationValue


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['text', 'rating']


class CompanyReviewForm(forms.ModelForm):
    class Meta:
        model = CompanyReview
        fields = ['delivery_quality', 'payment_quality', 'communication_quality', 'product_quality']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','slug','parent']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = ProductSpecification
        fields = '__all__'

class ProductSpecificationValueForm(forms.ModelForm):
    class Meta:
        model = ProductSpecificationValue
        fields = '__all__'


class ProductVideoForm(forms.ModelForm):
    class Meta:
        model = ProductVideo
        fields = ['video', 'alt_text', 'is_feature']





