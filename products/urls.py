from django.urls import path
from . import views

urlpatterns = [
    path("" , views.list_create_product_view, name="product-list"),
    path("<int:pk>/" , views.product_detailview, name="product-detail"),
    path("<int:pk>/update" , views.product_updateview, name="product-edit"),
    path("<int:pk>/delete" , views.product_deleteview ),
    path("<int:pk>/comment" , views.add_comment_view),
    path("<int:pk>/vote" , views.add_vote_view)
]

# urlpatterns = [
#     path("" , views.product_mixins_view),
#     path("<int:pk>/" , views.product_mixins_view),
#     path("<int:pk>/update" , views.product_mixins_view),
#     path("<int:pk>/delete" , views.product_mixins_view)
# ]