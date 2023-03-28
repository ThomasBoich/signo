from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *
from django.views.generic import TemplateView


router = DefaultRouter()
router.register('file', UploadDocsAPIViewSet)
# router.register('get_doc_to_frontend/<int:pk>', GetDocToFrontendAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),   
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),


]