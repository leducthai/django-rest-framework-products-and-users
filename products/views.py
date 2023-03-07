from rest_framework import generics , mixins , permissions
from .models import products
from .serializers import productserializer, ProductDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.mixins import StaffEditorPermissionMixin , UserQuerySetMixin
from api.serializer import commentser , voteseri
from rest_framework.views import APIView
import requests


class productdetailapiview(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = products.objects.all()
    serializer_class = ProductDetailSerializer

product_detailview = productdetailapiview.as_view()

class productupdateapiview(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = products.objects.all()
    serializer_class = productserializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ## not call save func again

product_updateview = productupdateapiview.as_view()

class productdeleteapiview(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = products.objects.all()
    serializer_class = productserializer
    lookup_field = "pk" # optional

    def perform_destroy(self, instance):
        # do s.t to the instance
        super().perform_destroy(instance)

product_deleteview = productdeleteapiview.as_view()

class productlistcreateapiview(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = products.objects.all()
    serializer_class = productserializer

    def perform_create(self, serializer):
        #serializer.save(user= self.request.user)
        #print(serializer.validated_data)
        
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if not content:
            content = title
        serializer.save(user= self.request.user, content = content)

    # def get_queryset(self, *args , **kwargs):
    #     qs = super().get_queryset( *args , **kwargs)
    #     request = self.request

    #     return qs.filter(user = request.user)
    
list_create_product_view = productlistcreateapiview.as_view()

class addcomment(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.CreateAPIView):
    serializer_class = commentser
    queryset = products.objects.all()
    
    def perform_create(self, serializer):
        comm = serializer.validated_data.get('comment')
        data = {
            'user_id': self.request.user.pk,
            'pd_id': self.kwargs.get('pk'),
            'comment': comm
        }
        rs = requests.post('http://172.23.0.3:8000/comment/' , json=data ).json()
        return Response(rs)
    
add_comment_view = addcomment.as_view()

class add_vote(APIView):

    def post(self, request , *args, **kwargs):
        inpu = request.data
        print(inpu)
        if not inpu:
            inpu['t'] = '1'
        inpu["user_id"] = request.user.pk
        inpu["pd_id"] = kwargs.get('pk')
        print(inpu)
        # try:
        #     data = voteseri(inpu).data
        # except:
        #     return Response({"status": "invalid input"}, status=400)
        
        rs = requests.post('http://172.23.0.3:8000/vote/' , json=inpu ).json()
        return Response(rs)
    
add_vote_view = add_vote.as_view()


class productMixinView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = products.objects.all()
    serializer_class = productserializer
    lookup_field = "pk"

    def get(self, request , *args , **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request ,pk=None, *args , **kwargs):
        return self.create(request , *args , **kwargs)

    def perform_create(self, serializer):
        #serializer.save(user= self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if not content:
            content = "hot content"
        serializer.save(content = content)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # do s.t to the instance
        super().perform_destroy(instance)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ## not call save funt again
    
product_mixins_view = productMixinView.as_view()

@api_view(['GET' , 'POST'])
def product_alt_view(request ,pk=None, *args , **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None :
            print('haha')
            queryset = get_object_or_404(products , pk=pk)
            data = productserializer(queryset , many= False).data
            return Response(data)
        queryset = products.objects.all()
        data = productserializer(queryset , many= True).data
        return Response(data)

    if method == "POST":
        serializer = productserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #data = serializer.save()
            #print(serializer.data)
            print(serializer.validated_data)
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content") or None
            if not content:
                content = title
            serializer.save(content = content)
            return Response(serializer.data)
        return Response({"invalid" : "not good data"} , status=400)       
