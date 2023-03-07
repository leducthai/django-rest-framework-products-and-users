from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(index_name= 'thai_products'):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query,*args ,**kwargs):
    index = get_index()
    params = {}
    index_filter = [f"{k}:{v}" for k , v in kwargs.items() if v] 
    if len(index_filter) != 0:
        params["facetFilters"] = index_filter
    result = index.search(query , params)
    return result