from django.urls import path

from documents.views import sign_document_finish
from users.views import login, registration, logout, AppLoginView, AppLogoutView, show_profile, doctors, users, \
    administrators, AppRegistration, show_mymedcard, user, usermedcard

urlpatterns = [
    path('login/', AppLoginView.as_view(), name='login'),
    path('registration/', AppRegistration.as_view(), name='registration'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('users/doctors/', doctors, name='doctors'),
    path('users/', users, name='users'),
    path('users/administrators/', administrators, name='administrators'),
    # path('profile/<int:pk>', ShowProfileView.as_view(), name='profile'),
    path('profile/', show_profile, name='profile'),
    path('mymedcard/', show_mymedcard, name='mymedcard'),
    path('user/<int:pk>/', user, name='user'),
    path('user/medcard/<int:pk>/', usermedcard, name='usermedcard'),
    path('documents/signed/sign/<int:pk>/', sign_document_finish, name='sign_document_finish'),
]