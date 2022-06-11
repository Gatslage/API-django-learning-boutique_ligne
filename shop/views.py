from unicodedata import category
from rest_framework.viewsets import ReadOnlyModelViewSet,ModelViewSet

from shop.serializers import categorySeria,productSeria,articleSeria
from shop.models import Category,Product,Article

class CategoryMViewSet(ReadOnlyModelViewSet):

    serializer_class=categorySeria

    def get_queryset(self):

        cat=Category.objects.all()
        st=self.request.GET.get('statut')

        return (cat.filter(active=True) if st=='active' else cat.filter(active=False)) if st is not None else cat
    


class ProductMViewSet(ReadOnlyModelViewSet):

    serializer_class=productSeria

    def get_queryset(self):
        prAc=Product.objects.all()
        st=self.request.GET.get('statut')
        prAc=( prAc.filter(active=True) if (st=='active') else prAc.filter(active=False)) if  (st is not None) else prAc
        c_id=self.request.GET.get('category_id')
        if c_id is not None :
            prAc=prAc.filter(category=c_id)

        return prAc
    
class ArticleMViewSet(ReadOnlyModelViewSet):

    serializer_class=articleSeria

    def get_queryset(self):

        p_id=self.request.GET.get('product_id')
        st=self.request.GET.get('statut')
        art=Article.objects.filter(product=p_id) if p_id!=None else Article.objects.all()
        return (art.filter(active=True) if st=='active' else art.filter(active=False)) if st!=None else art