from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *
from django.views.generic import TemplateView


router = DefaultRouter()
router.register('file', UploadDocsAPIViewSet)
# router.register('get_doc_to_frontend/<int:pk>', GetDocToFrontendAPIViewSet)
print('!!', router.get_urls())

urlpatterns = [
    path('', include(router.urls)),   
    # path('auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    # path('auth/login/', APILoginView.as_view(), name='api-login'),
    # path('auth/logout/', TemplateView.as_view(), name='api-logout'),
    path('auth/', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),


]