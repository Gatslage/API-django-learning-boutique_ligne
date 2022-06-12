from rest_framework.decorators import action
from rest_framework.response import Response
from unicodedata import category
from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet

from shop.serializers import categoryDetailSeria, categorySeria, productDetailSeria,productSeria,articleSeria
from shop.models import Category,Product,Article


class MultipleSerializerMixin():

    detail_serializer_class=None

    def get_serializer_class(self):
        if self.action=='retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class AdminCategoryMViewSet(MultipleSerializerMixin,ModelViewSet):
    serializer_class=categorySeria
    detail_serializer_class=categoryDetailSeria

    def get_queryset(self):

        return Category.objects.all()
class CategoryMViewSet(MultipleSerializerMixin,ReadOnlyModelViewSet):

    serializer_class=categorySeria
    detail_serializer_class=categoryDetailSeria

    def get_queryset(self):

        cat=Category.objects.all()
        st=self.request.GET.get('statut')
        return cat.filter(active=True)
        #return (cat.filter(active=True) if st=='active' else cat.filter(active=False)) if st is not None else cat
    @action(methods=['post'],detail=True)
    def disable(self,request,pk):
        self.get_object().disable()
        return Response()


class ProductMViewSet(MultipleSerializerMixin,ReadOnlyModelViewSet):

    serializer_class=productSeria
    detail_serializer_class=productDetailSeria


    def get_queryset(self):
        prAc=Product.objects.all()
        st=self.request.GET.get('statut')
        #prAc=( prAc.filter(active=True) if (st=='active') else prAc.filter(active=False)) if  (st is not None) else prAc
        c_id=self.request.GET.get('category_id')
        if c_id is not None :
            prAc=prAc.filter(category=c_id)

        return prAc.filter(active=True)

    @action(methods=['post'],detail=True)
    def disable(self,request,pk):
        self.get_object().disable()
        return Response()
    
class ArticleMViewSet(ReadOnlyModelViewSet):

    serializer_class=articleSeria

    def get_queryset(self):

        p_id=self.request.GET.get('product_id')
        st=self.request.GET.get('statut')
        art=Article.objects.filter(product=p_id) if p_id!=None else Article.objects.all()
        return (art.filter(active=True) if st=='active' else art.filter(active=False)) if st!=None else art

    @action(detail=True,methods=['post'])
    def disable(self,request,pk):
        art=self.get_object()
        art.disable()
        return Response()
class AdminArticleMViewSet(MultipleSerializerMixin,ModelViewSet):
    serializer_class=articleSeria

    def get_queryset(self):
        return Article.objects.all()