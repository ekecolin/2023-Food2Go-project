from io import open_code
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class APIUser(AbstractUser):
    pass

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True)
    ingredients = models.TextField(null=True)
    nutritional_information = models.TextField(null=True)
    macros = models.TextField(null=True)
    allergens = models.TextField(null=True)
    recipe = models.TextField(null=True)
    price = models.DecimalField(max_digits=6 , decimal_places=2, default=0.0) # 9999.99
    image = models.FileField(upload_to='products', null=True)

class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    # If you delete user delete their shopping basket + everything associated with them
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class BasketItem(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    # If I dont tell you how many I'm ordering assume its 1
    quantity = models.IntegerField(default=1)

    def product_name(self):
        return self.product_id.name

    # Calculating price of an item times the quantity
    def price(self):
        return self.product_id.price * self.quantity

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    sname = models.TextField(default="")
    # Auto default to current date & time - once order is made it will stamp time
    date_ordered = models.DateTimeField(auto_now_add=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6 , decimal_places=2, default=0.0)
    shipping_address = models.TextField(default="")
    city = models.TextField(default="")
    country = models.TextField(default="")
    postcode = models.TextField(default="")


class WeightTracking(models.Model):
    id = models.AutoField(primary_key=True)
    user= models.ForeignKey(APIUser, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(default=timezone.now)
    weightkg = models.DecimalField(max_digits=5, decimal_places=2, default = 0.0) #0 -> 999.99

class Recommendations(models.Model):
    id = models.AutoField(primary_key=True)
    left_hand_side = models.TextField()
    right_hand_side = models.IntegerField()

