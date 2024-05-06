from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class Login(models.Model):
    user_type=models.CharField(max_length=30)
    view_password=models.CharField(max_length=50)
    view_email=models.CharField(max_length=50)
    is_active =models.CharField(max_length=30,default=1)
class Seller(models.Model):
    username = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    sname = models.CharField(max_length=30, null= True)
    semail = models.EmailField(null=True)
    sphone = models.CharField(max_length=30, null= True)
    seller_pimage = models.FileField(null= True)
    s_status=models.CharField(max_length=30,default='Approved')
    
class Customer(models.Model):
    username = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    cname = models.CharField(max_length=30, null= True)
    cemail = models.EmailField(max_length=30,null=True)
    cphone = models.CharField(max_length=30, null= True)
    customer_pimage = models.FileField(null= True)
    c_status=models.CharField(max_length=30,default='Approved')

class Products(models.Model):
    productSeller = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    pname = models.CharField(max_length=30, null= True)
    pcategory = models.CharField(max_length=30, null= True)
    pdetails = models.CharField(max_length=30, null= True)
    bidDate = models.DateField()
    pemail = models.EmailField(null=True)
    price = models.CharField(max_length=30)
    productBidstatus = models.CharField(max_length=20, default='pending')


class BidTable(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    bidAmount = models.CharField(max_length=30)
    bidstatus = models.CharField(max_length=20, default='pending')
    seller_id = models.CharField(max_length=30)

class Chat(models.Model):
    uid = models.ForeignKey(Seller, on_delete=models.CASCADE)
    artistid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)

class onlineAuction(models.Model):
    productSeller = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    pname = models.CharField(max_length=30, null= True)
    pcategory = models.CharField(max_length=30, null= True)
    pdetails = models.CharField(max_length=30, null= True)
    bidDate = models.DateField()
    bidTime = models.TimeField(null=True)
    ampm = models.CharField(max_length=2, null= True)
    pemail = models.EmailField(null=True)
    price = models.CharField(max_length=30)
    productBidstatus = models.CharField(max_length=20, default='requested')
class auctionroom(models.Model):
    uid = models.ForeignKey(Seller, on_delete=models.CASCADE)
    artistid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bid = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)
    pid = models.CharField(max_length=100)

class onlineAuctionBidTable(models.Model):
    uid = models.CharField(max_length=300)#seller
    artistid = models.CharField(max_length=300)#customer
    bid = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    pid = models.CharField(max_length=100)
    semail = models.CharField(max_length=100)
    cemail= models.CharField(max_length=100)
    sphone= models.CharField(max_length=10)
    cphone= models.CharField(max_length=10)
    sname= models.CharField(max_length=100)
    cname= models.CharField(max_length=100)
    pname = models.CharField(max_length=30,null= True )