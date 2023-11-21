from django.shortcuts import redirect
from django.urls import resolve

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:          
            resolve(request.path_info)
        except:          
            return redirect('vendors:add-product-dashboard')

        return self.get_response(request)
