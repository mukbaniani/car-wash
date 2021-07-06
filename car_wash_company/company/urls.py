from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('create-order', views.OrderCreate, basename='order-create')

urlpatterns = [ 
    path('branch-list/', views.BranchList.as_view(), name='branch-list'),
    path('branch-detail/<int:pk>/', views.BranchDetail.as_view(), name='branch-detail'),
    path('washer-detail/', views.WasherDetail.as_view(), name='washer-datail'),
    path('washer-finish-task/', views.WasherFinishTask.as_view(), name='washer-finish-task')
] + router.urls