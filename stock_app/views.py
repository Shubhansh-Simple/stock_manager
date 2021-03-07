from .models              import Dates,Total,Stock,Icecream
from .forms               import StockCreateForm, StockUpdateForm
from Icecream.helper      import CheckEntryInModel

from django.contrib.auth.mixins    import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib                import messages
from django.http                   import HttpResponseRedirect
from django.shortcuts              import get_list_or_404
from django.urls                   import reverse
from django.views.generic          import ListView,\
                                          CreateView,\
                                          UpdateView

class IcecreamListView( ListView ):
    '''All icecreams in our database with their prices and pieces.'''

    model               = Icecream
    template_name       = 'icecream_list.html'
    context_object_name = 'icecream_list'


class DateListView( LoginRequiredMixin, ListView ):
    '''Only those dates in which stock entry made.'''

    paginate_by         = 30
    model               = Dates 
    template_name       = 'entry_list.html'
    context_object_name = 'entry_list'
    
    def get_queryset( self ):
        return Dates.objects.filter(id__in={ 
                                     x['entry_date_id'] 
                                     for x in Stock.objects.values()
                                   })


class StockListView( LoginRequiredMixin, ListView, CheckEntryInModel ):
    #Shows all stocks as per recieving dates.#
    
    model               = Stock
    template_name       = 'stock_list.html'
    context_object_name = 'stock_list'
    
    # MAGIC OF CLASS VARIABLE
    _stock = None


    def get_queryset( self ):
        '''All dates in which stock data modify by adding/removing.'''

        self._stock = get_list_or_404( Stock, entry_date__id=self.kwargs['pk'] )
        return self._stock


    def get_context_data( self,**kwargs ):

        context               = super( StockListView, self )\
                                     .get_context_data( **kwargs )
        
        # date of that day.
        context['entry_date'] = Dates.objects.get(
                                                   id=self.kwargs['pk']
                                                 ).entry_date
                                    
        context['is_today_date'] = self.is_today_date( context['entry_date'] )
        
        # that date total sale
        context['today_total_sale'] = sum([
                                            x.todays_sale for x in self._stock
                                         ])
        return context


class StockCreateView( LoginRequiredMixin, 
                       SuccessMessageMixin, 
                       CreateView,
                       CheckEntryInModel
                     ):

    model           = Stock
    template_name   = 'stock_create.html'
    form_class      = StockCreateForm
    success_message = 'Successfully Added'

    
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
                _stock = Stock.objects.get( 
                                             total     = int( FORM['total'] ),
                                             entry_date=FORM['entry_date']
                                           )
                _stock.arrival_boxes += int( FORM['arrival_boxes'] )
                _stock.save()

                _total.total_boxes += int( FORM['arrival_boxes'] )
                _total.save()
                
                messages.add_message( request,messages.ERROR, 
                                      'Successfully Added'  )

                # since we don't want to create Stock entry of today's date
                return HttpResponseRedirect( reverse('current_stock') )

            except Stock.DoesNotExist:
                '''If Stock table don't exist then create it using form procedure'''

                _total.total_boxes += int( FORM['arrival_boxes'] )
                _total.save()
                
                return self.form_valid(form)
        else:
            print( form.errors )
            return self.form_invalid(form)


class StockUpdateView( LoginRequiredMixin, UpdateView, CheckEntryInModel ):
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

class CurrentStockView( LoginRequiredMixin, ListView ):
    #Total Quantities present right now#

    model               = Total
    template_name       = 'current_stock_list.html'
    context_object_name = 'current_stock_list'
    
    # MAGIC OF CLASS VARIABLE 
    _total = None

    def get_queryset( self ):
        self._total = Total.objects.filter( total_boxes__gt=0 )
        return self._total


    def get_context_data( self,**kwargs ):
        '''Sending today's date to the Create Page.'''

        context               = super( CurrentStockView, self )\
                                     .get_context_data( **kwargs )
       
        # cost of all current stock 
        context['current_stock_total_price'] = sum([
                                            x.current_boxes_price 
                                            for x in self._total 
                                          ])
        return context














