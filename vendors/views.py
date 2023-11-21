from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from store.models import Product, ProductImage,Category,ProductType

from account.forms import RegistrationForm

from django.utils.text import slugify

from django.shortcuts import render, redirect
from .forms import ProductForm, ProductTypeForm, ProductSpecificationForm, ProductSpecificationValueForm, CategoryForm, ProductImageForm

from django.urls import reverse

from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory



from django.urls import resolve

def custom_404(request, exception):
    print('exception............=',exception)
    try:       
        resolve(request.path_info)
    except: 
        return redirect('vendors:add-product-dashboard')
    return render(request, 'vendors/add_product/404.html', status=404)


from django.urls import resolve
from django.shortcuts import render, redirect




def add_product_dashboard(request): 
    return render(request, 'vendors/add_product/add_product_dashboard.html')


def add_product_step1(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        product_type_form = ProductTypeForm(request.POST)      

        if all(form.is_valid() for form in [category_form, product_type_form]):
            category = category_form.save()
            product_type_form.save()           
            return redirect('vendors:add-product-step2', category_id=category.id)
    else:
        category_form = CategoryForm()
        product_type_form = ProductTypeForm()

    return render(request, 'vendors/add_product/add_product_step1.html', {
        'category_form': category_form,
        'product_type_form': product_type_form,
    })


def add_product_step2(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        specification_form = ProductSpecificationForm(request.POST)

        if all(form.is_valid() for form in [product_form, specification_form]):
            product = product_form.save(commit=False)
            product.category = category
            product.save()
            specification_form.save() 

            return redirect('vendors:add-product-step3', product_id=product.id)           
    else:
        product_form = ProductForm()
        specification_form = ProductSpecificationForm()

    return render(request, 'vendors/add_product/add_product_step2.html', {
        'product_form': product_form,
        'specification_form': specification_form,
    })



def add_product_step3(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        specification_value_form = ProductSpecificationValueForm(request.POST)

        if specification_value_form.is_valid():
            specification_value = specification_value_form.save(commit=False)
            specification_value.product = product
            specification_value.save()

            # Redirect to the next step or finish
            return redirect('vendors:add-product-step4', product_id=product.id)
    else:
        specification_value_form = ProductSpecificationValueForm()

    return render(request, 'vendors/add_product/add_product_step3.html', {
        'specification_value_form': specification_value_form,
    })


def add_product_step4(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)

    if request.method == 'POST':
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect('vendors:add-product-step4',product_id=product.id)
    else:
        formset = ProductImageFormSet(instance=product)

    return render(request, 'vendors/add_product/add_product_step4.html', {'formset': formset})



# first submission>> Category and product type = form-1 
# second submission>> product and specification = form-2
# third submission>> specification value = form-3
# fourth submission>> product image = form-4



def vendors(request):
    return render(request, 'vendors/vendors.html')


def become_vendor(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            # vendor = Vendor.objects.create(name=user.username, created_by=user)
            return redirect('store:store_home')
    else:
        form = RegistrationForm()   

    return render(request, 'vendors/become_vendor.html', {'form': form})


@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False


    return render(request, 'vendors/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)

#         if form.is_valid():
#             product = form.save(commit=False) 
#             product.vendor = request.user.vendor
#             product.slug = slugify(product.title)
#             product.save() 

#             return redirect('vendors:vendor-admin')

#     else:
#         form = ProductForm

#     return render(request, 'vendors/add_product.html', {'form': form})


@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name  = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save

            return redirect('vendors:vendor-admin')

    return render(request, 'vendors/edit_vendor.html', {'vendor': vendor})


# def vendors(request):
#     vendors = Vendor.objects.all()
#     return render(request, 'vendor/vendors.html', {'vendors': vendors})

# def vendor(request, vendor_id):
#     vendor = get_object_or_404(Vendor, pk=vendor_id)
#     return render(request, 'vendor/vendor.html', {'vendor': vendor})

