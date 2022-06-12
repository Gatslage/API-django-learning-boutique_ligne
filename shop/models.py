from django.db import models,transaction
import requests


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)



    def __str__(self):
        return self.name
    @transaction.atomic
    def disable(self):
        if self.active==False:
            return
        self.active=False
        self.save()
        self.products.update(active=False)


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')    
    def call_extern_api(self,method,url):
        return requests.request(method=method,url=url)
    @property
    def ecoscore(self):
        res=self.call_extern_api('GET','https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
        if res.status_code==200:
            return res.json()['product']['ecoscore_grade']

    def __str__(self):
        return self.name
    @transaction.atomic
    def disable(self):
        if self.active==False:
            return
        self.active=False
        self.save()
        self.articles.update(active=False)


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name

    @transaction.atomic
    def disable(self):
        if self.active==False:
            return
        self.active=False
        self.save()
        
        
