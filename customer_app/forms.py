from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django  import forms

from .models import Customer

class CustomerCreationForm( UserCreationForm ):

    class Meta( UserCreationForm.Meta ):
        model  = Customer
        fields = UserCreationForm.Meta.fields


class CustomerChangeForm( UserChangeForm ):

    class Meta:
        model  = Customer
        fields = UserChangeForm.Meta.fields


class CustomerCreateForm( forms.ModelForm ):
    class Meta:
        model   = Customer
        fields  = (
                    'first_name','last_name','location',
                  )









