from rest_framework import generics
from products.models import products
from products.serializers import productserializer
from . import client
from rest_framework.response import Response


class SearchListView(generics.GenericAPIView):
    def get(self, request , *args , **kwargs):
        query = request.GET.get('q')
        if not query:
            query = ''
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        published = str(request.GET.get('published')) not in ["0", "False"]
        # if not query:
        #     return Response("kkk" , status=400)
        result = client.perform_search(query , user=user , published=str(published))
        return Response(result)

class SearchListOldView(generics.ListAPIView):
    queryset = products.objects.all()
    serializer_class = productserializer

    def get_queryset(self , *args , **kwargs):
        qs = super().get_queryset(*args , **kwargs)
        q = self.request.GET.get('q')   
        result = products.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            result = qs.search(q , user= user)
        return result
