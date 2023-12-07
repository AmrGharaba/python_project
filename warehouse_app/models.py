from django.db import models
import re

class Usermanager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = 'passwrd should be at least eight characters'
        if postData['password'] != postData['confrim_password']:
            errors['password'] = 'passwrod must match'
        if User.objects.filter(email = postData['email'] ):
            errors['email'] = "Account already exists"
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        if len(postData['first_name']) < 2:
            errors['last_name'] = 'first name must be at least 2 characters'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Usermanager()

class Inventory(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    image = models.TextField()
    count = models.IntegerField(default=1000)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Store(models.Model):
#     name = models.CharField(max_length=45)
#     description = models.TextField()
#     location = models.CharField(max_length=45)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     item = models.ManyToManyField(Inventory, through = 'Shipment')

class Category(models.Model):
    name = models.CharField(max_length=45)
    items = models.ManyToManyField(Inventory, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Shipment(models.Model):
#     item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)

