from django.views.generic          import ListView,\
                                          CreateView #,\
                                          #UpdateView

from django.contrib.auth           import get_user_model
from django.contrib                import messages
from django.shortcuts              import render 
from django.http                   import HttpResponseRedirect
from django.db.models              import Sum
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins    import LoginRequiredMixin

# local
from .models          import Supply
from .forms           import SupplyCreateForm
from Icecream.helper  import CheckEntryInModel

# another app
from stock_app.models import Stock,Dates


class SupplyCreateView( LoginRequiredMixin,
                        SuccessMessageMixin, 
                        CreateView, 
                        CheckEntryInModel ):
    '''
        Combine Customer with Stock items
        then decrease total boxes entries.
    '''

    model                 = Supply
    template_name         = 'supply_create.html'
    form_class            = SupplyCreateForm
    success_message       = 'Successfully Supplied'

    # MAGIC OF CLASS VARIABLE
    _customer,_entry_date = None,None


    def dispatch( self, request, *args, **kwargs ):
        '''Check weather the customer exist or not first.'''

        self._customer = self.existence_of_customer( 
                                                    self.kwargs['pk'] 
                                                   )
        self._entry_date   = self.existence_of_date()

        return super( SupplyCreateView, self ).dispatch( request, *args, **kwargs)
  

    def post( self, request, *args, **kwargs ):
        '''Modify 3 Stock,Total & Supply models together'''

        FORM = request.POST.copy()

        
        FORM['entry_date'] = self._entry_date.id
        FORM['customer']   = self._customer.id

        form = self.form_class( FORM )

        if form.is_valid():
            
            print('Form is valid brother.')
            # TOTAL MODEL
            _total = self.existence_of_total( int(FORM['total']) )

            _total.total_boxes -= int( FORM['order_boxes'])

            # raise error if the demanded value is greater than availabe
            _total.save()

            # STOCK MODEL
            try:
                _stock  = Stock.objects.get( 
                                              total      = int( FORM['total'] ),
                                              entry_date = FORM['entry_date']
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

                               entry_date    = self._entry_date,
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

                messages.add_message( request,messages.ERROR, 
                                      'Successfully Supplied'  )
                
                # redirect to same page with message
                return HttpResponseRedirect( self.request.path_info )

            except Supply.DoesNotExist:
                # create supply entry using form procedure.
                return self.form_valid( form )

        else:
            print('Form is invalid brother')
            print( form.errors )
            #return self.form_invalid(form)
            return render( request, 'supply_create.html',
                           { 'form' : form, 'customer' : self._customer } )


    def get_context_data( self,**kwargs ):
        # Sending Customer instance

        context               = super( SupplyCreateView, self )\
                                     .get_context_data( **kwargs )

        context['customer']   = self._customer
        context['entry_date'] = self._entry_date.id

        return context


class CustomerChooseListView( LoginRequiredMixin, ListView ):
    '''Choose customer to supply stock.'''

    model               = get_user_model()
    template_name       = 'choose_customer.html'
    context_object_name = 'choose_customer'

    def get_queryset( self ):
        return get_user_model().objects.filter( password='' )


class CustomerSupplyEntryListView( LoginRequiredMixin, CheckEntryInModel, ListView ):
    '''Dates in which stock supply to customer'''
    
    paginate_by         = 30
    model               = Supply
    template_name       = 'customer_supply_entry_list.html'
    context_object_name = 'customer_supply_entry'

    # MAGIC OF CLASS VARIABLE
    _customer = None

    def get_queryset( self ):
        '''Set comprehension with validation of customer id'''

        self._customer = self.existence_of_customer( self.kwargs['pk'] )

        return Dates.objects.filter( id__in= 
                { 
                    x.entry_date.id 
                    for x in Supply.objects.filter( 
                        customer = self._customer
                    )
                } # set ends
            )

    def get_context_data( self,**kwargs ):
        '''Sending customer instance'''

        context               = super( CustomerSupplyEntryListView, self )\
                                     .get_context_data( **kwargs )

        context['customer']   = self._customer
        return context


###############################
#### Customer Bill Section ####
###############################

class CustomerBillView( LoginRequiredMixin, CheckEntryInModel, ListView ):
    '''Customer Bill as per dates.'''

    # /<int:pk>/estimate/<int:customer_id>/

    model               = Supply
    template_name       = 'sample_bill.html'
    context_object_name = 'sample_bill'
    
    # MAGIC OF CLASS VARIABLE
    _customer, _entry_date, _supply = None,None,None


    def get_queryset( self ):
        '''All supply of each Customer with specific date.'''

        self._customer   = self.existence_of_customer( self.kwargs['customer_id'] )
        self._entry_date = self.exist_date__or_not( self.kwargs['pk'] )

        self._supply     = Supply.objects.filter( 
                                       customer   = self._customer.id,
                                       entry_date = self._entry_date.id
                                    )
        return self._supply


    def get_context_data( self,**kwargs ):
        '''It's a heavy page do alot of calculation.'''

        context                    = super( CustomerBillView , self )\
                                                  .get_context_data( **kwargs )
        
        # Customer Model
        context['customer']        = self._customer

        # Dates Model
        context['entry_date']      = self._entry_date

        # Supply Model
        context['order_boxes_sum'] = self._supply.aggregate( 
                                                            Sum('order_boxes') 
                                                           )['order_boxes__sum']
        # per flavour sale
        context['total_customer_sale'] = sum([  
                                               x.each_icecream_sale 
                                               for x in self._supply 
                                            ])

        # each flavour have 40% disscount
        context['discount_amount'] = context['total_customer_sale'] -\
                                         ( context['total_customer_sale'] * 0.4 )

        return context









