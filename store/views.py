from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from django.views.generic import ListView
from .models import ProductReview
from .forms import CompanyReviewForm
from django.shortcuts import redirect
from .forms import ProductReviewForm
from fuzzywuzzy import fuzz
from django.contrib.admin.views.decorators import user_passes_test


def product_all(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)  
    categories = Category.objects.all()  
    product_stars = []
    for product in products:
        reviews = product.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / len(reviews)
            product.stars = get_stars(average_rating)   
            product_stars.append(product.stars)        
        else:
            product.stars = None  # Set stars to None if there are no reviews for the product          
    return render(request, "store/index.html", {'categories': categories, 'products': products,'product_stars':product_stars})



def get_stars(rating):
    full_stars = int(rating)
    half_stars = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars
    return '★' * full_stars + '½' * half_stars + '☆' * empty_stars



def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)  

    for product in products:
        reviews = product.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / len(reviews)
            product.stars = get_stars(average_rating)           
        else:
            product.stars = None 

    return render(request, "store/category.html", {"category": category, "products": products})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True) 
    specifications = product.productspecificationvalue_set.all()
    reviews = product.reviews.all()
    if reviews:
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / len(reviews)
        product.stars = get_stars(average_rating)           
    else:
        product.stars = None   
   
    return render(request, "store/single.html", {"product": product, "specifications": specifications})
    


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  
        context['products'] = Product.objects.all()  
             
        return context
  



def search(request):
    query = request.GET.get('q')
    predefined_answers = {
        "What is the product return policy?": "Our product return policy allows customers to return products within 30 days of purchase.",
        "How can I track my order?": "You can track your order by logging into your account and visiting the 'Order History' section.",
        "What payment methods do you accept?": "We accept all major credit cards and PayPal for payment.",
        # Add more predefined questions and answers here
    }

    answer = None
    for predefined_question, predefined_answer in predefined_answers.items():
        if fuzz.partial_ratio(predefined_question.lower(), query.lower()) > 80:
            answer = predefined_answer
            break

    if answer:
        return render(request, 'store/search_new.html', {'answer': answer, 'query': query})
    else:
        results = Product.objects.filter(title__icontains=query).order_by('-id') if query else Product.objects.none()
        return render(request, 'store/search_new.html', {'results': results, 'query': query})



def product_reviews(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
          
            return redirect('store:company-reviews')
    else:
        form = ProductReviewForm()
    return render(request, 'store/product_reviews.html', {'form': form})



def read_product_reviews(request, slug):  
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = ProductReview.objects.filter(product=product)
    return render(request, "store/read_product_reviews.html", {'product': product, 'reviews': reviews})


#  submit company review
def company_reviews(request):
    form = CompanyReviewForm()
    if request.method == 'POST':
        form = CompanyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user 
            # Set the user here if needed
            review.save()
            # Handle successful form submission
            return redirect('store:store_home')
    context = {'form': form}
    return render(request, 'company_review.html', context)    
    
  
def read_company_reviews(request):
    pass

  