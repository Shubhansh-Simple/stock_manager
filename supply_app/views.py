from django.views.generic          import ListView,\
                                          CreateView #,\
                                          #UpdateView
from django.contrib.auth           import get_user_model
from django.http                   import HttpResponseRedirect 
from django.db.models              import Sum
from django.contrib.messages.views import SuccessMessageMixin

# local
from .models          import Supply
from .forms           import SupplyCreateForm
from .helper2         import CheckEntryInModel

# another app
from stock_app.models import Stock,Dates
from stock_app.helper import AllAboutDate


class SupplyCreateView( SuccessMessageMixin, CreateView, AllAboutDate, CheckEntryInModel ):
    '''
        Combine Customer with Stock items
        then decrease total boxes entries.
    '''
    model               = Supply
    template_name       = 'supply_create.html'
    form_class          = SupplyCreateForm
    success_message     = 'Successfully Supplied Brother'
   

    def post( self, request, *args, **kwargs ):
        '''Modify 3 Stock,Total & Supply models together'''

        FORM = request.POST.copy()

        FORM['entry_date'] = self.existence_of_date().id
        FORM['customer']   = self.kwargs['pk']

        form = self.form_class( FORM )

        if form.is_valid():
            
            # TOTAL MODEL
            _total = self.existence_of_total( int(FORM['total']) )
            _total.total_boxes -= int( FORM['order_boxes'])
            _total.save()

            # STOCK MODEL
            try:
                _stock  = self.existence_of_stock( 
                                                   int( FORM['total'] ),
                                                   FORM['entry_date']
                                                 )
                _stock.sold_boxes += int(FORM['order_boxes'])
                _stock.remain_boxes = _total.total_boxes
                

            #If Stock table don't exist then follow form procedure
            except Stock.DoesNotExist:
                '''Want to create stock instance through fields.'''

                _stock = Stock.objects.create(
                                # this is a bug which need repair.
                               total         = _total,
                               current_boxes = _total.total_boxes +\
                                               int( FORM['order_boxes'] ),

                               entry_date    = Dates.objects\
                                                    .get( 
                                                        id=FORM['entry_date'] 
                                                        ),
                               sold_boxes    = int(FORM['order_boxes']),
                               remain_boxes  = _total.total_boxes
                            )
            _stock.save()
                
            # Supply MODEL
            try:
                _supply = Supply.objects.get( 
                                             customer   = FORM['customer'],
                                             total      = FORM['total'],
                                             entry_date = FORM['entry_date']
                                            )
                _supply.order_boxes += int( FORM['order_boxes'] )
                _supply.save()
                
                # redirect to same page with message
                return HttpResponseRedirect( self.request.path_info )
                                           

            except Supply.DoesNotExist:
                # create supply entry using form procedure.
                return self.form_valid( form )

        else:
            print( form.errors )
            return self.form_invalid(form)


    def get_context_data( self,**kwargs ):
        # Adding Customer instance

        context               = super( SupplyCreateView, self )\
                                     .get_context_data( **kwargs )

        context['customer'] = get_user_model().objects.get( id=self.kwargs['pk'] )

        return context


class CustomerChooseListView( ListView ):
    '''Choose customer to supply stock.'''

    model               = get_user_model()
    template_name       = 'choose_customer.html'
    context_object_name = 'choose_customer'

    def get_queryset( self ):
        return get_user_model().objects.filter( password='' )


class CustomerSupplyEntryListView( ListView ):
    '''A Customer Supplied all Dates List'''

    model = Supply
    template_name = 'customer_supply_entry_list.html'
    context_object_name = 'customer_supply_entry'

    # enter date here
    def get_queryset( self ):
        return Dates.objects.filter( id__in= { 
               x.entry_date.id 
               for x in Supply.objects.filter( customer=self.kwargs['pk']) 
            })

        '''
        UNDER CONSTRUCTION
        return Dates.objects.filter( id__in={
                x.entry_date.id for x in Supply.objects.filter( customer=self.kwargs['pk'])
            })
        '''

    def get_context_data( self,**kwargs ):

        context               = super( CustomerSupplyEntryListView, self )\
                                     .get_context_data( **kwargs )

        context['customer'] = get_user_model().objects.get( id=self.kwargs['pk'] )

        return context


class CustomerBillView( ListView ):
    '''Customer Bill as per dates.'''

    # /<int:pk>/estimate/<int:customer_id>/

    model               = Supply
    template_name       = 'sample_bill.html'
    context_object_name = 'sample_bill'

    def get_queryset( self ):
        '''All supply of each Customer with specific date.'''

        return Supply.objects.filter( 
                                      customer   = self.kwargs['customer_id'],
                                      entry_date = self.kwargs['pk'] 
                                    )

    def get_context_data( self,**kwargs ):
        '''It's a heavy page do alot of calculation.'''

        context                    = super( CustomerBillView , self )\
                                                  .get_context_data( **kwargs )
        
        # Customer Model
        context['customer']        = get_user_model().objects.get( 
                                                    id=self.kwargs['customer_id'] 
                                                         )

        # Dates Model
        context['entry_date']      = Dates.objects.get( id=self.kwargs['pk'] )

        # Supply Model
        context['order_boxes_sum'] = Supply.objects.filter( 
                                      customer   = self.kwargs['customer_id'],
                                      entry_date = self.kwargs['pk'] 
                                      ).aggregate( 
                                                    Sum('order_boxes') 
                                                 )['order_boxes__sum']

        context['total_customer_sale'] = sum([  
                                          x.each_icecream_sale \
                                          for x in Supply.objects.filter( 
                                          customer   = self.kwargs['customer_id'],
                                          entry_date = self.kwargs['pk']
                                                                        ) 
                                         ])

        context['discount_amount'] = context['total_customer_sale'] -\
                                         ( context['total_customer_sale'] * 0.4 )


        return context


'''
MAY BE LATER
don't use this view
class SupplyListView( ListView ):

    model               = Dates 
    template_name       = 'supply_entries.html'
    context_object_name = 'supply_list'
    
    def get_queryset( self ):
        ''Those dates in which supply occured.''
        
        return Dates.objects.filter(id__in={ 
                                x[4] for x in Supply.objects.values_list() 
                                   })
'''












