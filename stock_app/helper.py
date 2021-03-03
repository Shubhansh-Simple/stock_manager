'''
    Just make the views.py clean 
    we create this file and keep the custom helper
    class separate from view
'''
from datetime import datetime
from .models  import Dates,Total


class AllAboutDate():
    '''Here the Date means Date Model.'''

    def existence_of_date( self ):
        '''Get|Create Dates Model object,given date not exists'''

        return Dates.objects.\
                 get_or_create( entry_date=datetime.now().date() )[0]


    def is_today_date( self,date_plz ):
        return datetime.now().date() == date_plz


    def existence_of_total( self, total_id ):
        '''This items present 100 and 10%.'''

        return Total.objects.get( id = total_id )



  





