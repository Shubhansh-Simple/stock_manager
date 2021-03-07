from django.urls import path
from .views      import SupplyCreateView,\
                        CustomerBillView,\
                        CustomerChooseListView,\
                        CustomerSupplyEntryListView

app_name = 'supply_app'

urlpatterns = [
    #path('',                 SupplyListView.as_view(),   name='supply_list' ),
    path('create/<int:pk>/', SupplyCreateView.as_view(), name='supply_create' ),

    path('choose', CustomerChooseListView.as_view(), name='choose_customer_record'),

    path('<int:pk>/estimate/', 
          CustomerSupplyEntryListView.as_view() , name='choose_customer'),

    path('<int:pk>/estimate/<int:customer_id>/', 
          CustomerBillView.as_view(), name='customer_bill' ),

  ] 



