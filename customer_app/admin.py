from django.contrib            import admin
from django.contrib.auth.admin import UserAdmin

from .forms  import CustomerChangeForm , CustomerCreationForm
from .models import Customer

class CustomerAdmin( UserAdmin ):
    add_form  = CustomerCreationForm
    form      = CustomerChangeForm
    model     = Customer

admin.site.register( Customer,CustomerAdmin )

