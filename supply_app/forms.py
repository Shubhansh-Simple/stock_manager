from django                 import forms
from django.core.exceptions import ValidationError
from .models                import Supply

from stock_app.models import Total


class SupplyCreateForm( forms.ModelForm ):

    class Meta:
        model = Supply

        fields  = ( 'customer', 'total','order_boxes', 'entry_date',)

        widgets = {
                    'customer'   : forms.widgets.HiddenInput(),
                    'entry_date' : forms.widgets.HiddenInput(),
                  }

        labels  = {
                    'total'       : 'Select Icecream',
                    'order_boxes' : 'Supplied Quantity'
                  }


    def __init__( self, *args, **kwargs ):
        '''Only show availabe ice-cream on supplying.'''

        super( SupplyCreateForm, self).__init__(  *args, **kwargs )
        self.fields['total'].queryset = Total.objects.filter( total_boxes__gt=0 )


