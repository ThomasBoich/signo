from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('file', UploadDocsAPIViewSet)
urlpatterns = [
    # path('files/', UploadDocsAPIView.as_view(), name='index'),
    path('', include(router.urls)),    
]