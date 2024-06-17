from django.urls import path
from rest_framework import routers


from .views import *

router = routers.SimpleRouter()

router.register('products', ProductViewSet, 'products')

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='all_orders'),
    path('myorders/<int:pk>/', UpdateOrderView.as_view(), name='order_update'),
    path('soldOut/', SoldOutListView.as_view(), name='sold_out'),
    path('products/<int:pk>/addorder/', CreateOrderView.as_view(), name='add_order'),
    path('myorders/', GetUserOrderListView.as_view(), name='my_order'),
]

urlpatterns += router.urls
