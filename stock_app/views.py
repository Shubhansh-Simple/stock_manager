from .models              import Dates,Total,Stock
from .forms               import StockCreateForm, StockUpdateForm
from .helper              import AllAboutDate 

from supply_app.helper2   import CheckEntryInModel

##from django.contrib       import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http                   import HttpResponseRedirect #, HttpResponse
from django.urls                   import reverse
from django.views.generic          import ListView,\
                                          CreateView,\
                                          UpdateView


class DateListView( ListView ):
    #Showing Dates through Stock Model#

    model               = Dates 
    template_name       = 'entry_list.html'
    context_object_name = 'entry_list'
    
    def get_queryset( self ):
        
        return Dates.objects.filter(id__in={ 
                                x[7] for x in Stock.objects.values_list() 
                                   })


class StockListView( ListView, AllAboutDate ):
    #Shows all stocks as per recieving dates.#

    model               = Stock
    template_name       = 'stock_list.html'
    context_object_name = 'stock_list'


    def get_queryset( self ):
        return Stock.objects.select_related('total')\
                    .filter( entry_date__id=self.kwargs['pk'] )


    def get_context_data( self,**kwargs ):

        context               = super( StockListView, self )\
                                     .get_context_data( **kwargs )

        context['entry_date'] = Dates.objects.get(
                                                   id=self.kwargs['pk']
                                                 ).entry_date
                                    
        context['is_today_date'] = self.is_today_date( context['entry_date'] )

        context['today_total_sale'] = sum([
                                            x.todays_sale
                                            for x in Stock.objects.filter( 
                                            entry_date__id=self.kwargs['pk'] )
                                         ])
        return context


class StockCreateView( SuccessMessageMixin, CreateView, AllAboutDate, CheckEntryInModel ):
    model         = Stock
    template_name = 'stock_create.html'
    form_class    = StockCreateForm
    success_message = 'Successfully added icecream'

    
    def post( self,request,*args,**kwargs ):
        '''Make the input data ready for the hidden fields'''

        FORM = request.POST.copy()

        FORM['entry_date']    = self.existence_of_date().id
        _total                = self.existence_of_total( int(FORM['total']) )

        FORM['current_boxes'] = _total.total_boxes

        form = self.form_class( FORM )

        if form.is_valid():
            
            #If Stock table already exist then only modify arrival boxes
            try:
                _stock = self.existence_of_stock( 
                                                 int( FORM['total'] ),
                                                 FORM['entry_date']
                                               )
                _stock.arrival_boxes += int( FORM['arrival_boxes'] )
                _stock.save()

                _total.total_boxes += int( FORM['arrival_boxes'] )
                _total.save()

                # since we don't want to create Stock entry of today's date
                # by following form procedure

                return HttpResponseRedirect( 
                                   reverse('current_stock') #,
                                           #args=[ str( FORM['entry_date'] )]
                                          )#)

            #If Stock table don't exist then follow form procedure
            except Stock.DoesNotExist:

                _total.total_boxes += int( FORM['arrival_boxes'] )
                _total.save()
                
                # this create the Stock instance
                return self.form_valid(form)
        else:
            print( form.errors )
            return self.form_invalid(form)


class StockUpdateView( UpdateView, AllAboutDate ):
    '''Can only modify arrival stock of today's date only.'''

    model               = Stock
    form_class          = StockUpdateForm
    template_name       = 'stock_create.html'
    context_object_name = 'stock_list'
   

    def get_context_data( self,**kwargs ):
        '''Sending today's date to the Create Page.'''

        context               = super( StockUpdateView, self )\
                                     .get_context_data( **kwargs )
        self.object           = self.get_object()
        
        # we first check it's the today's date or not.
        #self.is_today_date( self.object.entry_date )

        context['entry_date'] = self.object.entry_date.entry_date
        return context


    def post( self, request, *args, **kwargs ):

        self.object           = self.get_object()
        FORM = request.POST.copy()
        
        self.object.total.total_boxes = self.object.current_boxes +\
                                        int( FORM['arrival_boxes'] )

        request.POST = FORM

        return super( StockUpdateView,self ).post( request,*args,**kwargs )


#######################
## Total Stock Model ##
#######################

class CurrentStockView( ListView ):
    #Total Quantities present right now#

    model               = Total
    template_name       = 'current_stock_list.html'
    context_object_name = 'current_stock_list'

    def get_queryset( self ):
        return Total.objects.filter( total_boxes__gt=0 )


    def get_context_data( self,**kwargs ):
        '''Sending today's date to the Create Page.'''

        context               = super( CurrentStockView, self )\
                                     .get_context_data( **kwargs )
       
        # cost of all current stock 
        context['total_stock_price'] = sum([
                                            x.current_boxes_price 
                                            for x in Total.objects.filter
                                            ( total_boxes__gt=0 ) 
                                          ])
        return context














