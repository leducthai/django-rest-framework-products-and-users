from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import products
from .validator import unique_product_title , no_thai_in_title
from api.serializer import UserPublicSerializer, commentser, voteseri
import requests

class productserializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source= 'user',read_only= True)
    url = serializers.SerializerMethodField(read_only= True)
    edit_url = serializers.HyperlinkedIdentityField(
        view_name="product-edit",
        lookup_field = "pk" 
    )
    votes = serializers.SerializerMethodField(read_only= True)
    comments = serializers.SerializerMethodField(read_only= True)
    title = serializers.CharField(validators=[unique_product_title , no_thai_in_title])
    #email = serializers.EmailField(write_only= True)
    class Meta:
        model = products
        fields = [
            'owner',
            'edit_url',
            'url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'published',
            'votes',
            'comments'
        ]

    # def validate_title(self , value):
    #     qs = products.objects.filter(title__iexact = value)
    #     print(qs)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a title !")
    #     return value

    # def create(self, validated_data):
    #     email = validated_data.pop("email")
    #     obj =  super().create(validated_data)
    #     return obj

    # def update(self, instance, validated_data):
    #     email = validated_data.pop("email")
    #     instance.title = validated_data.get("title")
    #     return super().update(instance, validated_data)

    def get_my_user(self, obj):
        return {
            "username" : obj.user.username
        }

    def get_url(self, obj):
        request = self.context.get("request") 
        if not request:
            return None
        return reverse("product-detail" , kwargs={"pk" : obj.pk} , request=request)

    def get_feel(self, obj):
        if not hasattr(obj , "id"):
            return None
        if not isinstance(obj , products):
            return None
        return obj.new_def()
    
    def get_votes(self , obj):
        qs = requests.get('http://172.23.0.3:8000/vote/?pd=%s' % obj.pk).json()
        if qs:
            return len(qs)
        return None
    
    def get_comments(self, obj):
        qs = requests.get('http://172.23.0.3:8000/comment/?pd=%s' % obj.pk).json()
        if qs:
            return len(qs)
        return None



class ProductDetailSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source= 'user',read_only= True)
    votes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = products
        fields = [
            'owner',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'published',
            'votes',
            'comments'
        ]
    
    def get_votes(self , obj):
        return voteseri(requests.get('http://172.23.0.3:8000/vote/?pd=%s' % obj.pk).json() , many=True).data
    
    def get_comments(self, obj):
        return commentser(requests.get('http://172.23.0.3:8000/comment/?pd=%s' % obj.pk).json() , many=True).data

