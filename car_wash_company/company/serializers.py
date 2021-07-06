from rest_framework import serializers
from .models import Branch, CarType, Order, Washer
from django.utils import timezone
from .fields import IsFreeField


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class BranchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%Y-%m-%d-%M")

    class Meta:
        model = Order
        fields = ['order_date', 'user', 'branch', 'car_type']

    def validate(self, attrs):
        branch = attrs.get('branch')
        today = timezone.now()
        order_date = attrs.get('order_date')
        if today > order_date:
            raise serializers.ValidationError(f'{order_date} დღე დამთავრებულია შეკვეთის გაკეთება შეგიძლია მხოლოდ დღეს ან მომვალ დღეებში')
        if branch.garage_amount == 0:
            raise serializers.ValidationError('ყველა ადგილი დაკავებული')
        return attrs

    def create(self, validated_data):
        branch = validated_data.get('branch')
        washer = Washer.objects.get_random_washer(branch)
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
        if instance.is_finished is True:
            raise serializers.ValidationError('შეკვეთა დასრულებულია')
        branch = validated_data.get('branch')
        instance.order_date = self.validated_data.get('order_date')
        instance.car_type = self.validated_data.get('car_type')
        if branch != instance.branch:
            washer = Washer.objects.get_random_washer(branch)
            instance.washer.profite -= instance.car_type.wash_price * instance.washer.part / 100
            instance.washer.is_free = True
            instance.washer.save()
            instance.washer = washer
            instance.washer.profite += instance.car_type.wash_price * instance.washer.part / 100
            instance.washer.is_free = False
            instance.washer.save()
            instance.branch = branch
        instance.save()
        return instance


class WasherDetailSerializer(serializers.Serializer):
    future_plan = serializers.CharField(read_only=True)
    washed_car = serializers.CharField(read_only=True)

    class Meta:
        fields = ['future_plan', 'washer_car']


class WasherFinishTaskSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')
    part = serializers.SerializerMethodField('get_part')
    is_free = IsFreeField()

    class Meta:
        model = Washer
        fields = ['id', 'part', 'is_free']

    def get_id(self, obj):
        return obj.get('id')

    def get_part(self, obj):
        return obj.get('part')

    def get_is_free(self, obj):
        return obj.get('is_free')