from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('<slug:c_slug>/',views.home,name='home_category'),
    path('<slug:c_slug>/<slug:p_slug>',views.product_details,name='details'),
    path('search',views.search,name='search'),
    path('cart',views.cart, name = 'cart'),
    path('addcart/<int:product_id>/',views.add_cart,name='addcart'),
    path('mincart/<int:product_id>/',views.min_cart,name='mincart'),
    path('deletecart/<int:product_id>/',views.cart_delete,name='deletecart'),
    path('accounts/login/',views.log_in,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.log_out,name='logout')
]