from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('title',
                  'price',
                  'description',
                  'category')


class ExpenseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('title',
                  'price',
                  'description',
                  'category',
                  'account',
                  'date_created')
        depth = 1
