from .serializers import BranchSerializer, OrderSerializer, BranchDetailSerializer
from rest_framework import generics, permissions, viewsets
from .models import Branch, CarType, Order
from .permissions import CanDelete


class BranchList(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetail(generics.ListAPIView):
    serializer_class = BranchDetailSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('pk')
        queryset = CarType.objects.filter(branch=branch_id).all()
        return queryset


class OrderCreate(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, CanDelete]