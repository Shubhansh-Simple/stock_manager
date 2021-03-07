from django           import forms
from .models          import Supply
from stock_app.models import Total
from Icecream.helper  import CheckEntryInModel


class SupplyCreateForm( forms.ModelForm, CheckEntryInModel ):

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

    def clean( self ):

        if self.cleaned_data.get('total').total_boxes < \
           self.cleaned_data.get('order_boxes'):

           raise forms.ValidationError('We have only {} boxes left'.format( 
                                       self.cleaned_data.get('total').total_boxes ) 
                                      )
        return self.cleaned_data



















