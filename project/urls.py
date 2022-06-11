from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.views import CategoryMViewSet,ProductMViewSet,ArticleMViewSet

router=routers.SimpleRouter()

router.register('category',CategoryMViewSet,basename='category')
router.register('product',ProductMViewSet,basename='product')
router.register('article',ArticleMViewSet,basename='article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include(router.urls))
]
