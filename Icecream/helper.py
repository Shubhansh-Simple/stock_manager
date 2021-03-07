'''
    Just make the views.py clean 
    we create this file and keep the custom helper
    class separate from view
'''

from django.shortcuts    import get_object_or_404
from django.contrib.auth import get_user_model
from datetime            import datetime
from stock_app.models    import Stock,Dates,Total


class CheckEntryInModel():
    '''Check Entries exist or not in models'''


    # CUSTOMER MODEL Raise Error
    def existence_of_customer( self, customer_id ):
        '''If customer not found then raise 404 error'''

        return get_object_or_404( get_user_model(), pk=customer_id , password='' )


    # STOCK MODEL Raise Error
    def existence_of_stock( self, total_id, entry_date_id ):
        '''Check stock entry exist or not otherwise raise 404.'''

        return get_object_or_404(
                                  Stock,
                                  total     =total_id,
                                  entry_date=entry_date_id
                                ) 
    
    # TOTAL MODEL Raise Error
    def existence_of_total( self, total_id ):
        '''This items present 100 and 10%.'''

        return get_object_or_404( Total, pk=total_id )


    # DATE MODEL
    def existence_of_date( self ):
        '''Get/Create Dates Model object,if given date not exists'''

        return Dates.objects.\
                 get_or_create( entry_date=datetime.now().date() )[0]


    # DATE MODEL Raise Error
    def exist_date__or_not( self, date_id ):
        '''Raise 404 if the date_id not exist.'''

        return get_object_or_404( Dates, pk = date_id )

    
    def is_today_date( self,date_plz ):
        return datetime.now().date() == date_plz


    
