from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from .forms import * 
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics
from .utils import get_recommendations_for_user
import random


# Create your views here.
def register(request):
    return render(request, 'register.html')

def index(request):
    return render(request, 'index.html')

def chart(request):
    return render(request, 'chart.html')

def weightloss(request):
    lossproducts = Product.objects.all()
    r_products = []
    if request.user.is_authenticated:
        user = request.user
        r_products = get_recommendations_for_user(user) # get recommendations
    print(r_products)
    return render(request, 'weightloss.html', {'lossproducts':lossproducts, 'recommendations':r_products})

def staylean(request):
    leanproducts = Product.objects.all()
    r_products = []
    if request.user.is_authenticated:
        user = request.user
        r_products = get_recommendations_for_user(user) # get recommendations
    print(r_products)
    return render(request, 'staylean.html', {'leanproducts':leanproducts, 'recommendations':r_products})

def bulk(request):
    bulkproducts = Product.objects.all()
    r_products = []
    if request.user.is_authenticated:
        user = request.user
        r_products = get_recommendations_for_user(user) # get recommendations
    print(r_products)
    return render(request, 'bulk.html', {'bulkproducts':bulkproducts, 'recommendations':r_products})

def order(request):
    return render(request, 'order.html')

def bmi(request):
    return render(request, 'bmi.html')

def ourmenu(request):
    return render(request, 'ourmenu.html')

# Getting individual product information from django
def foodproducts(request, prodid):
    # get the product with id = prodid
    product = Product.objects.get(id=prodid)
    recipe_steps = product.recipe.split("=")
    return render(request, 'foodproducts.html', {'product': product, 'recipe_steps': recipe_steps})

class UserSignupView(CreateView):
    model = APIUser
    form_class = UserSignupForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLoginView(LoginView):
    template_name='login.html'
    
def logout_user(request):
    logout(request)
    return redirect("/")
    
def open_view(request):
    ... # Anyone can access this view
        
@login_required
def locked_view(request):
    ... # only logged in users can get here
    
@login_required
def add_to_basket(request, prodid):
    user = request.user
    # is there a shopping basket for the user 
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        # create a new one
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # get the product 
    product = Product.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        # there is no basket item for that product 
        # # create one 
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        # a basket item already exists 
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return render(request, 'foodproducts.html', {'product': product, 'added':True})

@login_required
def show_basket(request):
    # get the user object
    # does a shopping basket exist ? -> your basket is empty
    # load all shopping basket items
    # display on page
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    r_products = get_recommendations_for_user(user) # get recommendations
    print(r_products)
    if basket is None:
        #TODO: basket is empty
        return render(request, 'index.html', {'empty': True})
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        # is this list empty ?
        if sbi.exists():
            # normal flow
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi, 'recommendations':r_products})
        else:
            #TODO: show empty basket
            return render(request, 'basket.html', {'empty': True, 'recommendations':r_products}) # pass to front end

@login_required
def remove_item(request, sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect('/basket') #error redirect to shopping basket
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity-1
            basketitem.save() #save pur changes to the db
        else:
            basketitem.delete() #delete the basket item
    return redirect('/basket')

@login_required
def order(request):
    # load in all data we need, user, basket, items
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # If there are no items in the shopping basket the user is redirected to the homepage
    if basket is None:
        return redirect("/")
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists(): #if there are no items
        # WANT TO MAKE HTML SAY BASKET IS EMPTY
        return redirect("/")
    # POST or GET
    if request.method == 'POST':
        # check if valid
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = 0.0
            for item in sbi:
                total += float(item.price())
            order.total_price = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order':order, 'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})
    else:
        # show the form
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders':orders})

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class BasketViewSet(viewsets.ModelViewSet):
  serializer_class = BasketSerializer
  queryset = Basket.objects.all()
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
      user = self.request.user # get the current user
      if user.is_superuser:
          return Basket.objects.all() # return all the baskets if a superuser requests
      else:
          # For normal users, only return the current active basket
          shopping_basket = Basket.objects.filter(user_id=user, is_active=True)
          return shopping_basket

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user # get the current user
        if user.is_superuser:
            return Order.objects.all() # return all the baskets if a superuser requests
        else:
            # For normal users, only return the current active basket
            orders = Order.objects.filter(user_id=user)
            return orders

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = APIUser.objects.all()
    serializer_class = APIUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserRegistrationAPIViewSet(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] #No login is needed to access this route
    queryset = queryset = APIUser.objects.all()

class AddBasketItemAPIView(generics.CreateAPIView):
    serializer_class = AddBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

class RemoveBasketItemAPIView(generics.CreateAPIView):
    serializer_class = RemoveBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

class CheckoutAPIView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()


@login_required
def weight_loss(request):
    user =  request.user
    user_logged_weights = WeightTracking.objects.filter(user=user).order_by('date_logged')
    labels = [] # week numbers
    loss = []#actual weights
    for w in user_logged_weights:
        labels.append(w.date_logged.isocalendar().week)
        loss.append(float(w.weightkg))

    if request.method=="POST":
        form = WeightLossForm(request.POST)
        if form.is_valid():
            nweight = form.save(commit=False)
            nweight.user = user
            nweight.save()
            return redirect('weight_loss')
        else:
            return render(request, 'chart.html', {'weight_labels':labels , 'weight_loss': loss, 'form':form})
    else:
        form = WeightLossForm()
    return render(request, 'chart.html', {'weight_labels':labels , 'weight_loss': loss, 'form':form})


@login_required
def reset_weight(request):
    user =  request.user
    WeightTracking.objects.filter(user=user).delete()
    return redirect('weight_loss')