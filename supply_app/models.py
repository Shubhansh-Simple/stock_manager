from django.db   import models
from django.conf import settings
from django.urls import reverse

from stock_app.models import Dates,Total


class Supply( models.Model ):
    '''Supplied stock to customers,according to dates'''

    customer       = models.ForeignKey( settings.AUTH_USER_MODEL,
                                        on_delete=models.PROTECT )

    total          = models.ForeignKey( Total, on_delete=models.PROTECT )
    order_boxes    = models.PositiveSmallIntegerField()
    entry_date     = models.ForeignKey( Dates, on_delete=models.PROTECT )

    @property
    def each_icecream_sale( self ):
        '''Sale of each icecream by customer'''

        return self.total.icecream.per_box_price * self.order_boxes


    def get_absolute_url( self ):
        '''We will redirect to that Date in which stock is created.'''
        
        return reverse('supply_app:supply_create',
                        args=[ str(self.customer.id) ] )

   
    def __str__( self ):
        return '{} - {} {}'.format( self.customer,self.total,self.entry_date )



