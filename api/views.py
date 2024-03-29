import json
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django.http import JsonResponse
from django.forms.models import model_to_dict
from products.models import products
from products.serializers import productserializer
from .serializer import logoutserializer, signupAPIseri
from django.contrib.auth.models import User

@api_view(["GET"])
def aip_home(request , *args , **kwargs):
    instance = products.objects.all().order_by("?").first()
    data = {}
    if instance:
        #data = model_to_dict(model_data , fields=['id' ,'title', 'price', 'sale_price'])
        data = productserializer(instance).data
    return Response(data)

@api_view(["POST"])
def api_home(request , *args , **kwargs):
    serializer = productserializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        #data = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid" : "not good data"} , status=400)
# def aip_home(request , *args , **kwargs):
#     body = request.body
#     print(request.GET) #url query params
#     print(request.POST)
#     data = {}
#     try:
#         data = json.loads(body)
#     except:
#         pass
#     print(data)
#     data["params"] = dict(request.GET)
#     data["headers"] = dict(request.headers)
#     data["content_type"] = request.content_type
#     return JsonResponse(data)


class logoutview(generics.GenericAPIView):
    serializer_class = logoutserializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()

        return Response(status=204)
    
logoutAPIview = logoutview.as_view()


class signupAPIview(generics.GenericAPIView):
    serializer_class = signupAPIseri

    def post(self, request , *args , **kwargs):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception= True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        User.objects.create_superuser(username= username, password= password)

        return Response(status=200)
    
signupsuper = signupAPIview.as_view()