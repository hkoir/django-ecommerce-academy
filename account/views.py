from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders
from store.models import Product

from .forms import RegistrationForm, UserAddressForm, UserEditForm,ProfilePictureForm
from .models import Address, Customer
from .tokens import account_activation_token
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import user_passes_test

from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/dashboard.html", {"section": "profile", "orders": orders})


@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


from django.views.decorators.http import require_POST

# @require_POST................ this is view is original but added user type condition only and is postponed due to email verification issues.
# def account_register(request):
#     if request.user.is_authenticated:
#         return redirect("account:dashboard")
    
#     if request.method == "POST":
#         register_form = RegistrationForm(request.POST)
#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.email = register_form.cleaned_data["email"]
#             user.set_password(register_form.cleaned_data["password"])

#             if user.user_type == 'seller':
#                 user.is_active = False  # Admin approval required for staff
#             else:
#                 user.is_active = True

#             user.save()

#             current_site = get_current_site(request)
#             subject = "Activate your Account"
#             message = render_to_string(
#                 "account/registration/account_activation_email.html",
#                 {
#                     "user": user,
#                     "domain": current_site.domain,
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "token": account_activation_token.make_token(user),
#                 },
#             )
#             user.email_user(subject=subject, message=message)

#             return render(request, "account/registration/register_email_confirm.html", {"form": register_form})
#     else:
#         register_Form = RegistrationForm()
#     return render(request, "account/registration/register.html", {"form": register_Form})


# below is the temporary account register form until email-server is managed
# def account_register(request):
#     if request.user.is_authenticated:
#         return redirect("account:dashboard")    
#     if request.method == "POST":
#         register_form = RegistrationForm(request.POST)
#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.email = register_form.cleaned_data["email"]
#             user.set_password(register_form.cleaned_data["password"])
#             user.is_active =True        
#             user.save()          
#             login(request, user)
#             messages.success(request, 'Registration successful. You are now logged in.')
#             return redirect("account:dashboard")
#     else:
#         register_form = RegistrationForm()
#     return render(request, "account/registration/register.html", {"form": register_form})


# below view is temporary activation without sending email checking due email server not available.
# def account_activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = Customer.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         if user.user_type == 'seller':           
#             user.is_active = True
#         else:          
#             user.is_active = False

#         user.save()
#         login(request, user)
#         return redirect("account:dashboard")
#     else:
#         return render(request, "account/registration/activation_invalid.html")

#below is the original view but postponed due to email verifications issue
# def account_activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = Customer.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, user.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect("account:dashboard")
#     else:
#     
#     return render(request, "account/registration/activation_invalid.html")





# initial version code
def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


# initial version code
def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user =Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')










class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'admin':
             return reverse_lazy('store:store_home')  
        elif user.user_type == 'staff':
             return reverse_lazy('store:product-list') 
        elif user.user_type == 'seller':             
            return reverse_lazy('account:dashboard') 
        else:
            print("Nothing happens")
            return super().get_success_url()
        

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        else:
            return super().get_success_url()
        
       
    


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses")




def update_profile_picture(request, user_id):
    user = get_object_or_404(Customer, pk=user_id)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:dashboard')  # Redirect to the appropriate page after successful update

    else:
        form = ProfilePictureForm(instance=user)

    return render(request, 'account/change_profile_picture.html', {'form': form})




@user_passes_test(lambda u: u.is_staff)
def admin_view(request):
    user_id = request.user.id
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    user_name = user.name

    videox = Product.objects.all()

    if not request.user.is_staff:     
        messages.error(request, "You are not authorized to view this page.")  
        return HttpResponseRedirect(reverse("login"))
     
    return render(request, 'account/admin/admin_page.html', {'user': user_name,'videox':videox})

   