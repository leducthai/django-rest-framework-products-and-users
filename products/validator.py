from .models import products
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

def validate_title(value):
    qs = products.objects.filter(title__iexact = value)
    print(qs)
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a title !")
    return value

def no_thai_in_title(value):
    if 'thai' in value.lower():
        raise serializers.ValidationError("thai can be in title !")

unique_product_title = UniqueValidator(queryset=products.objects.all(), lookup='iexact')