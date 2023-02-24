from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('file', UploadDocsAPIViewSet)
# router.register('get_doc_to_frontend/<int:pk>', GetDocToFrontendAPIViewSet)


urlpatterns = [
    # path('files/', UploadDocsAPIView.as_view(), name='index'),
    path('', include(router.urls)),    
]