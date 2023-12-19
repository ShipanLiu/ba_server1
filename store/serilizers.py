from rest_framework import serializers
from .models import Customer

# Customized SLizer for Customer
class CustomerModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date"]

    user_id = serializers.IntegerField()