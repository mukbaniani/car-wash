from . import views
from django.urls import path


urlpatterns = [ 
    path('register/', views.RegisterUser.as_view(), name='register-user'),
    path('login/', views.LoginUser.as_view(), name='login-user'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password-reset-request', views.PasswordResetRequest.as_view(), name='password-reset-request'),
    path('update-password/<str:uidb64>', views.PasswordUpdate.as_view(), name='update-password')
]