from django.db import models
#from django.contrib.auth import models
from django.contrib.auth.models import User

# Create your models here.

# class Demo(models.Model):
#     email=models.EmailField(max_length=50)
    
#     password=models.CharField(max_length=50)

# class Product(models.Model):
#     name=models.CharField(max_length=50)
#     price=models.IntegerField()
#     cat=models.IntegerField()
#     product_details=models.CharField(max_length=500)
#     is_active=models.BooleanField(default=True)

#     def __str__(self) -> str:
#         return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    
   

class Product(models.Model):
    CAT=((1, "mobile"),(2,"shoes"),(3,"cloths"))
    name=models.CharField(max_length=50, verbose_name="Product name")
    price=models.IntegerField()
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    product_details=models.CharField(max_length=500, verbose_name="Product Details")
    is_active=models.BooleanField(default=True, verbose_name="Available")
    p_img=models.ImageField(upload_to='image')

    # def __str__(self) -> str:
    #     return self.name

class Cart(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete = models.CASCADE, db_column = 'user_id')
    pid = models.ForeignKey('Product', on_delete = models.CASCADE, db_column = 'pid')
    qty = models.IntegerField(default = 1)

class Order(models.Model):
    order_id = models.CharField(max_length = 100)
    user_id = models.ForeignKey('auth.User', on_delete = models.CASCADE, db_column = 'user_id')
    pid = models.ForeignKey('Product', on_delete = models.CASCADE, db_column = 'pid')
    qty = models.IntegerField(default = 1)
    amt = models.FloatField()

class MyOrder(models.Model):
    order_id = models.CharField(max_length = 100)
    user_id = models.ForeignKey('auth.User', on_delete = models.CASCADE, db_column = 'user_id')
    pid = models.ForeignKey('Product', on_delete = models.CASCADE, db_column = 'pid')
    qty = models.IntegerField(default = 1)
    amt = models.FloatField()


class Address(models.Model):
    # first_name = models.CharField(max_length=50, blank=False, null=False)
    # last_name = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # foreign key to user table
    address = models.CharField(max_length=80, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)

# class data(models.Model):
#     user_id = models.ForeignKey('auth.User', on_delete = models.CASCADE, db_column = 'user_id')
#     pid = models.ForeignKey('Address', on_delete = models.CASCADE, db_column = 'pid')
#     address = models.ForeignKey('Address', on_delete = models.CASCADE, db_column = 'address')
#     contact = models.ForeignKey('Address', on_delete = models.CASCADE, db_column = 'phone_number')

# class info(models.Model):
#     user_id = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'user_id')
#     address = models.CharField(max_length=80, blank=False, null=False)
#     phone_number = models.CharField(max_length=15, blank=False, null=False)
    
class info_data(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    address = models.CharField(max_length=80, blank=False, null=False)
    city = models.CharField(max_length=80, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)