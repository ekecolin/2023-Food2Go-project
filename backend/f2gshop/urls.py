from django.urls import include, path
from . import views
from f2gshop.forms import *
from .forms import UserSignupForm, UserLoginForm
from rest_framework import routers

# 127.0.0.1:8000/products/
router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'basket', views.BasketViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'users', views.APIUserViewSet)

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
    path('logout/', views.logout_user, name="logout"),
    path('products/<int:prodid>', views.foodproducts, name = "foodproducts"),
    path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
    path('basket/', views.show_basket, name="show_basket"),
    path('removeitem/<int:sbi>', views.remove_item, name="remove_item"),
    path('order/', views.order, name="order"),
    path('orderhistory/', views.previous_orders, name="order_history"),
    path('api/', include(router.urls)),
    path('apiregister/', views.UserRegistrationAPIViewSet.as_view(), name="api_register"),
    path('apiadd/', views.AddBasketItemAPIView.as_view(), name="api_add_to_basket"),
    path('apiremove/', views.RemoveBasketItemAPIView.as_view(), name="api_remove_from_basket"),
    path('apicheckout/', views.CheckoutAPIView.as_view(), name="api_checkout"),
    path('weighttracking', views.weight_loss, name="weight_loss"),
    path('resetweight', views.reset_weight, name="reset_weight"),
]
