from algoliasearch_django import AlgoliaIndex
from .models import products, User
from algoliasearch_django.decorators import register


@register(products)
class ProductIndex(AlgoliaIndex):
    #should_index = 'is_public'
    fields = [
        'title',
        'content',
        'price',
        'user',
        'published'
    ]
    settings = {
        "searchableAttributes" : ['title' , 'content'],
        "attributesForFaceting" : ['user' , 'published']
    }
    
# admin.site.register(products , ProductModelAdmin)
