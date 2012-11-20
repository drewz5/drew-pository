from  django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

class Address(models.Model):
    person = models.ForeignKey('Person', related_name='addresses')
    street_adress_1 = models.CharField(max_length=100)
    street_adress_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
