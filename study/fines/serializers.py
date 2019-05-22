from rest_framework import serializers
from study.models import *

from .models import Fine
from study.policies.serializers import PolicySerializer


class FineSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    policy = PolicySerializer(read_only=True)

    class Meta:
        model = Fine
        fields = ('id', 'amount', 'user', 'policy')
