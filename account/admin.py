from django.contrib import admin

from .models import Customer,Address

admin.site.register(Customer)
admin.site.register(Address)




# @admin.register(Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['customer', 'full_name', 'phone', 'postcode', 'address_line', 'address_line2', 'town_city', 'delivery_instructions', 'default', 'created_at', 'updated_at']

# admin.site.register(Address, AddressAdmin)


