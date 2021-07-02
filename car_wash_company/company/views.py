from datetime import datetime
from .serializers import BranchSerializer, OrderSerializer, BranchDetailSerializer, WasherDetailSerializer
from rest_framework import generics, permissions, viewsets
from .models import Branch, CarType, Order, Washer
from .permissions import CanDelete, IsWasher
from django.db.models import Count, Q


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


class WasherDetail(generics.ListAPIView):
    serializer_class = WasherDetailSerializer
    permission_classes = [IsWasher]

    def get_queryset(self):
        query = Washer.objects.filter(
            order__order_date__iso_year__gte=datetime.now().year, user=self.request.user
        ).annotate(
            washed_car = Count('order', Q(order__is_finished=True)),
            future_plan = Count('order', Q(order__is_finished=False))
        ).all()
        return query