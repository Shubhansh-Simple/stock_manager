from .models          import Supply
from stock_app.models import Stock


class CheckEntryInModel():
    '''Check Entries exist or not in models'''

    def existence_of_supply( self, total_id, customer_id, entry_date_id ):
        '''Check entry exist or not in Stock model.'''

        try:
            return Supply.objects.get(
                            total      = total_id,
                            customer   = customer_id,
                            entry_date = entry_date_id
                        )
        except Supply.DoesNotExist:
            return False


    def existence_of_stock( self, total_id, entry_date_id ):
        '''Check entry exist or not in Stock model.'''

        return Stock.objects.get( 
                                 total = total_id,
                                 entry_date = entry_date_id 
                                )
