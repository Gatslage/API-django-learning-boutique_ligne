from email.mime import base
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from shop.views import AdminArticleMViewSet, AdminCategoryMViewSet, CategoryMViewSet,ProductMViewSet,ArticleMViewSet

router=routers.SimpleRouter()

router.register('category',CategoryMViewSet,basename='category')
router.register('product',ProductMViewSet,basename='product')
router.register('article',ArticleMViewSet,basename='article')
router.register('admin-category',AdminCategoryMViewSet,basename='admin-category')
router.register('admin-article',AdminArticleMViewSet,basename='admin-article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include(router.urls)),
    path('api/token',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh')
]
