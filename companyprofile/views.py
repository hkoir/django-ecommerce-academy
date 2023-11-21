from django.shortcuts import render


def about(request):
    return render(request, 'companyprofile/about_us.html')

def contact(request):
    return render(request, 'companyprofile/contact_us.html')