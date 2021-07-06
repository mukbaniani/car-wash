from datetime import datetime
from rest_framework.response import Response
from .serializers import BranchSerializer, OrderSerializer, BranchDetailSerializer, WasherDetailSerializer, WasherFinishTaskSerializer
from rest_framework import generics, permissions, serializers, viewsets, views, status
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
    permission_classes = [permissions.IsAuthenticated, CanDelete]

    def get_queryset(self):
        query = Order.objects.filter(user=self.request.user).all()
        return query


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


class WasherFinishTask(views.APIView):
    permission_classes = [IsWasher]

    def get(self, request):
        washer = Washer.objects.filter(
            user=self.request.user
        ).values(
            'id', 'part', 'is_free'
        )
        serializer = WasherFinishTaskSerializer(washer, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        washer = Washer.objects.get(user=self.request.user)
        serializer = WasherFinishTaskSerializer(washer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if washer.is_free is False:
            print('\n\n\n', 1)
            washer.branch.garage_amount += 1
            washer.branch.save()
        serializer.save()
        return Response(status=status.HTTP_200_OK)