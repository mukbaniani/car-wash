from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('create-order', views.OrderCreate, basename='order-create')

urlpatterns = [ 
    path('branch-list/', views.BranchList.as_view(), name='branch-list'),
    path('branch-detail/<int:pk>/', views.BranchDetail.as_view(), name='branch-detail')
] + router.urls