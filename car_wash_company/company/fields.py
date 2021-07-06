from rest_framework import serializers


class IsFreeField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return data.capitalize()