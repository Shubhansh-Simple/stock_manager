from django.urls import path
from .views      import DateListView,\
                        StockCreateView,\
                        StockUpdateView,\
                        CurrentStockView,\
                        StockListView  

urlpatterns = [
    path('',                 DateListView.as_view(),  name='entry_list' ),
    path('<int:pk>/',        StockListView.as_view(), name='stock_list' ),
    path('<int:pk>/update/', StockUpdateView.as_view(), name='stock_update' ),

    path('create/', StockCreateView.as_view(),         name='stock_create' ),

   ## Total
   path('current_stock/', CurrentStockView.as_view(), name='current_stock' )
]
