from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',          include('stock_app.urls') ),
    path('accounts/', include('django.contrib.auth.urls') ),
    path('customer/', include('customer_app.urls') ),
    path('supply/',   include('supply_app.urls','supply_app') ),
]
