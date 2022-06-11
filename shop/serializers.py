import imp
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from shop.models import Category,Product,Article

class categorySeria(ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','active']

class productSeria(ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','date_created','date_updated','category','active']

class articleSeria(ModelSerializer):
    class Meta:
        model=Article
        fields=['id','name','date_created','date_updated','price','active','product']