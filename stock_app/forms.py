from django                 import forms
from .models                import Stock #,Icecream

class StockCreateForm( forms.ModelForm ):

    class Meta:
        model   = Stock
        fields  = (
                    'total','arrival_boxes',
                    'current_boxes','entry_date'
                  )

        widgets = {
                    'current_boxes' : forms.widgets.HiddenInput(),
                    'entry_date'    : forms.widgets.HiddenInput(),
                  }

        labels  = {
                    'total'         : 'Select Icecream',
                    'arrival_boxes' : 'Quantity'
                  }


    def __init__( self, *args, **kwargs ):
        '''Only show availabe ice-cream on supplying.'''

        super( StockCreateForm, self).__init__(  *args, **kwargs )
        self.fields['arrival_boxes'].initial = ''


class StockUpdateForm( forms.ModelForm ):

    icecreams = forms.CharField(
                    initial='Something',
                    widget=forms.TextInput(attrs={'readonly':'readonly'})
                )
    # add the entry_date fields it's very important
    # make the entry_date readonly it's very important.

    class Meta:
        model = Stock
        fields = ( 'icecreams','arrival_boxes','entry_date')


