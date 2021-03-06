from django.contrib import admin
from .models import Category, Product, Biders

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'ends', 'created', 'updated']
    list_filter = ['created', 'updated']
    list_editable = ['price','ends']
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Product, ProductAdmin)

# Register your models here.
