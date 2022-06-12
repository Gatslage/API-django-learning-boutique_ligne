
import requests
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from shop.models import Category,Product,Article

class categorySeria(ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description']

    def validate_name(self,value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('cette categorie existe deja')
        return value
    def validate(self, attrs):
        if attrs['name'] in attrs['description']:
            return attrs
        raise serializers.ValidationError('la description ne contient pas le nom de la categorie')
 

class categoryDetailSeria(ModelSerializer):
    products=serializers.SerializerMethodField()

    def get_products(self,instance):
        prods_own=instance.products.filter(active=True)
        seria=productSeria(prods_own,many=True)
        return seria.data
    class Meta:
        model=Category
        fields=['id','name','description','products']

class productSeria(ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','date_created','date_updated','category','ecoscore']


    

class productDetailSeria(ModelSerializer):
    articles=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','name','date_created','date_updated','category','articles']
    
    def get_articles(self,instance):
        art=instance.articles.filter(active=True)
        serializer=articleSeria(art,many=True)
        return serializer.data

class articleSeria(ModelSerializer):
    class Meta:
        model=Article
        fields=['id','name','date_created','date_updated','price','product']
    
    def validate(self, attrs):
        if attrs['price']<1 or attrs['product'].active!=True:
            raise serializers.ValidationError('le prix doit être superieur à 1 euro et le produit associé doit être actif')
        return attrs