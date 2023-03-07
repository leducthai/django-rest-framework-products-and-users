from rest_framework import serializers
from django.contrib.auth.models import User

class productInLine(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field = "pk" ,
        read_only= True
    )
    title = serializers.CharField(read_only= True)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only= True)
    id = serializers.IntegerField(read_only= True)
    # other_product = serializers.SerializerMethodField(read_only= True)

    def get_other_product(self , obj):
        usr = obj
        qs = usr.products_set.all()[:5]
        return productInLine(qs , many= True , context=self.context).data
    
class commentser(serializers.Serializer):
    cm_owner = serializers.SerializerMethodField(read_only=True)
    comment = serializers.CharField()

    def get_cm_owner(self , obj):
        u_id = obj.get('user_id')
        qs = User.objects.filter(pk = u_id).first()
        return UserPublicSerializer(qs).data

class voteseri(serializers.Serializer):
    vote_owner = serializers.SerializerMethodField(read_only=True)

    def get_vote_owner(self, obj):
        u_id = obj.get('user_id')
        qs = User.objects.filter(pk = u_id).first()
        return UserPublicSerializer(qs).data