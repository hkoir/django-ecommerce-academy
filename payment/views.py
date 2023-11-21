import json
import os

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.basket import Basket
from orders.views import payment_confirmation

from store.models import Product
from account.models import Address
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

import uuid
from basket.basket import Basket
from decimal import Decimal
from django.contrib.auth import get_user_model 




# def order_placed(request):
#     basket = Basket(request)
#     basket.clear()
#     return render(request, 'payment/orderplaced.html')


def order_placed(request):
    basket = Basket(request)
    for item in basket:
        product = item.get('product')
        product_qty = item.get('qty')
        if product.qty >= product_qty:  # Check if there is enough quantity available
            product.qty -= product_qty  # Reduce the available quantity
            product.save()  # Save the updated quantity to the database
        else:
            print(' do not have enough quantity')           
            messages.error(request, 'Not enough quantity available for {}'.format(product.title))
            return render(request, 'basket/summary.html')
            # return JsonResponse({'message': 'Order placed successfully'})           
          
    basket.clear()
    return render(request, 'payment/orderplaced.html')
   


class Error(TemplateView):
    template_name = 'payment/error.html'




@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    return render(request, 'payment/payment_form.html')

    # stripe.api_key = settings.STRIPE_SECRET_KEY
    # intent = stripe.PaymentIntent.create(
    #     amount=total,
    #     currency='bdt',
    #     metadata={'userid': request.user.id}
    # )

    # return render(request, 'payment/payment_form.html', {'client_secret': intent.client_secret, 
    #                                                         'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)





class checkout(TemplateView):
   template_name = "payment/check_out.html"
   model =Address 
   grandTotalPrice = 0 

   def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)        
        User = get_user_model()
        user = User.objects.get(pk=self.request.user.id)
        if user.is_authenticated:           
            context['customer_address'] =Address.objects.filter(customer=user)
        else:
            message_text= messages.warning(self.request, 'Please log in before checking out!')
            context['customer_address'] = message_text
       
        basket = Basket(self.request)
        context['total_price'] = basket.get_total_price()
        context['order_key'] = str(uuid.uuid4())      

        return context

 



def confirm_address(request):
    pass

def process_order(request):
    pass