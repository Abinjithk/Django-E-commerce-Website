from django.contrib import admin
from . models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','stock','image']
    list_editable = ['price','stock']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Products,ProductAdmin)
admin.site.register(Item)
admin.site.register(CartList)