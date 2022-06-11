from unicodedata import name
from urllib import response
from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from shop.models import Category,Product

class ShopAPITestCase(APITestCase):

    def format_dateTime(self,value):
        return value.strftime("%Y-%m-%d %H-%M-%S.%fZ")

class TestCategory(ShopAPITestCase):

    url=reverse_lazy('category')

    def test_list(self):
        cate=Category.objects.create(name='foster',active=True)
        Category.objects.create(name='oho oho',active=False)

        response=self.client.get(self.url)

        attendu=[{
            'name':cate.name,
            'id':cate.id,
            'date_created':self.format_dateTime(cate.date_created),
            'date_updated':self.format_dateTime(cate.date_updated)
        }]
        #verifications
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),attendu)


    def test_create(self):
        self.assertFalse(Category.objects.exists())

        res=self.client.post(self.url,data={'name':'ton','active':True})
        
        self.assertEqual(res.status_code,405)
        self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
    url=reverse_lazy('product')

    def test_list(self):

        prod=Product.objects.create(name='mon prod',active=True)
        Product.objects.create(name='dd',active=False)

        response=self.client.get(self.url)

        att=[{
            'name':prod.name,
            'id':prod.id,
            'date_created':self.format_dateTime(prod.date_created),
            'date_updated':self.format_dateTime(prod.date_updated)
        }]

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),att)

    def test_create(self):
        self.assertFalse(Product.objects.exists())

        res=self.client.post(self.url,data={'name':'blabla','active':'True'})
        self.assertEqual(res.status_code,405)
        self.assertFalse(Product.objects.exists())