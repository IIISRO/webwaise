from django.contrib import admin
from .models import Contact, Order, OrderRequest, Project, Product
# Register your models here.
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderRequest)
admin.site.register(Project)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']

admin.site.register(Product, ProductsAdmin)