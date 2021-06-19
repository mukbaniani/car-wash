from django.db.models import query
from rest_framework import serializers
from .models import Branch, CarType, Order, Washer
from datetime import datetime


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class BranchDetailSerializer(serializers.ModelSerializer):
    branch = serializers.SlugRelatedField(many=True, queryset=CarType.objects.all(), slug_field='address')

    class Meta:
        model = CarType
        fields = ['id', 'car_type', 'wash_price', 'branch']


class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Order
        fields = ['order_date', 'user', 'branch', 'car_type']

    def validate(self, attrs):
        branch = attrs.get('branch')
        today = datetime.now()
        order_date = attrs.get('order_date')
        if today > datetime(order_date.year, order_date.month, order_date.day):
            raise serializers.ValidationError(f'{order_date} დღე დამთავრებულია შეკვეთის გაკეთება შეგიძლია მხოლოდ დღეს ან მომვალ დღეებში')
        if branch.garage_amount == 0:
            raise serializers.ValidationError('ყველა ადგილი დაკავებული')
        return attrs

    def create(self, validated_data):
        branch = validated_data.get('branch')
        try:
            washer = Washer.objects.filter(branch_id=branch, is_free=True).order_by('?')[0]
        except:
            raise serializers.ValidationError('ყველა მრეცხავი დაკავებულია')
        order = Order(
            order_date=self.validated_data.get('order_date'),
            user=self.validated_data.get('user'),
            branch=self.validated_data.get('branch'),
            washer=washer,
            car_type=self.validated_data.get('car_type')
        )
        order.save()
        return order

    def update(self, instance, validated_data):
        branch = validated_data.get('branch')
        instance.order_date = self.validated_data.get('order_date')
        instance.car_type = self.validated_data.get('car_type')
        if branch != instance.branch:
            try:
                washer = Washer.objects.filter(branch_id=branch.id, is_free=True).order_by('?')[0]
                instance.washer.profite -= instance.car_type.wash_price * instance.washer.part / 100
                instance.washer.is_free = True
                instance.washer.save()
                instance.washer = washer
                instance.washer.profite += instance.car_type.wash_price * instance.washer.part / 100
                instance.washer.is_free = False
                instance.washer.save()
                instance.branch = branch
            except:
                raise serializers.ValidationError('ყველა მრეცხავი დაკავებულია')
        instance.save()
        return instance