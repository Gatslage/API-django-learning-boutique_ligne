from unittest import mock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy
from shop.mock import call_success_ecoscore

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):

    def setUp(self) -> None:
        return super().setUp()

    def format_dateTime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def category_json_transform(self, cats):
        return [{
            'id': cat.id,
            'name': cat.name,
            'description':cat.description,
            'products': self.products_json_transfrom(cat.products.filter(active=True))
        }for cat in cats]

    def products_json_transfrom(self, prods):
        return [{
            'name': prod.name,
            'id': prod.id,
            'date_created': self.format_dateTime(prod.date_created),
            'date_updated': self.format_dateTime(prod.date_updated),
            'category': prod.category.id,
            'articles': self.articles_json_transform(prod.articles.filter(active=True))
        } for prod in prods]

    def articles_json_transform(self, arts):
        return [{
            'id': art.id,
            'name': art.name,
            'price': art.price,
            'product': art.product.id
        }for art in arts]


class TestCategory(ShopAPITestCase):

    url = reverse_lazy('category-list')

    def test_list(self):
        cate = Category.objects.create(name='foster', active=True)
        Category.objects.create(name='oho oho', active=False)

        response = self.client.get(self.url)

        attendu = [{
            'id':cate.id,
            'name':cate.name,
            'description':cate.description
        }]
        # verifications
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), attendu)

        
    def test_detail_list(self):
        cate = Category.objects.create(name='foster', active=True)
        Category.objects.create(name='oho oho', active=False)

        response = self.client.get(reverse('category-detail', args=[cate.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual([response.json()],self.category_json_transform([cate]))
    def test_create(self):
        self.assertFalse(Category.objects.exists())

        res = self.client.post(self.url, data={'name': 'ton'})

        self.assertEqual(res.status_code, 405)
        self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
    url = reverse_lazy('product-list')
    @mock.patch('shop.models.Product.call_extern_api',call_success_ecoscore)
    def test_list(self):
        cat = Category.objects.create(name='pour_prod')
        prod = cat.products.create(name='mon prod', active=True)
        cat.products.create(name='dd', active=False)

        response = self.client.get(self.url)

        att = [{
            'id':prod.id,
            'name':prod.name,
            'category':cat.id,
            'date_created':self.format_dateTime(prod.date_created),
            'date_updated':self.format_dateTime(prod.date_updated),
            'ecoscore':prod.ecoscore
        }]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), att)

    
    def test_create(self):
        self.assertFalse(Product.objects.exists())

        res = self.client.post(
            self.url, data={'name': 'blabla', 'active': 'True'})
        self.assertEqual(res.status_code, 405)
        self.assertFalse(Product.objects.exists())
    @mock.patch('shop.models.Product.call_extern_api',call_success_ecoscore)
    def test_prod_part(self):
            cat=Category.objects.create(name='pour_prod2')
            prod=cat.products.create(name='mon prod2',active=True)
            Category.objects.create(name='oublie').products.create(name='dd',active=False)
            res=self.client.get(self.url+'?category_id=%i' %cat.id)
            att=[{
                'name':prod.name,
                'id':prod.id,
                'date_created':self.format_dateTime(prod.date_created),
                'date_updated':self.format_dateTime(prod.date_updated),
                'category':prod.category.id,
                'ecoscore':prod.ecoscore
            }]
            self.assertEqual(res.status_code,200)
            self.assertEqual(res.json(),att)
