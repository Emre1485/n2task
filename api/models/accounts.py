from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    website = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class Company(models.Model):
    user = models.OneToOneField('User', related_name='company', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Address(models.Model):
    user = models.OneToOneField('User', related_name='address', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.street}, {self.city}"
    
class Geo(models.Model):
    address = models.OneToOneField('Address', related_name='geo', on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"({self.lat}, {self.lng})"