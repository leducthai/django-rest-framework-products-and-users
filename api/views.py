import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django.http import JsonResponse
from django.forms.models import model_to_dict
from products.models import products
from products.serializers import productserializer

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


