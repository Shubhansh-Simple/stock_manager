from django.views.generic          import ListView,\
                                          CreateView,\
                                          UpdateView
from django.contrib.auth           import get_user_model
from django.http                   import HttpResponseRedirect
from django.urls                   import reverse
from django.contrib.auth.mixins    import LoginRequiredMixin

from .forms               import CustomerCreateForm
from .models              import Customer


class CustomerListView( LoginRequiredMixin, ListView ):
    model               = get_user_model()
    template_name       = 'customer_list.html'
    context_object_name = 'customer_list'

    def get_queryset( self ):
        return get_user_model().objects.filter( password='' )


class CustomerCreateView( LoginRequiredMixin, CreateView ):
    model         = get_user_model()
    template_name = 'customer_create.html'
    form_class    = CustomerCreateForm

    def post( self, request, *args, **kwargs ):

        FORM = request.POST.copy()

        FORM['first_name'] = FORM['first_name'].title() 
        FORM['last_name']  = FORM['last_name'].title() 
        FORM['location']   = FORM['location'].capitalize()

        form = self.form_class( FORM )

        if form.is_valid():
            Customer.objects.create(
                                    username   = FORM['first_name'],
                                    first_name = FORM['first_name'],
                                    last_name  = FORM['last_name'],
                                    location   = FORM['location']
                                   )

            return HttpResponseRedirect( reverse('customer_list') )

        else:
            print( form.errors )
            return self.form_invalid(form)

         
class CustomerUpdateView( LoginRequiredMixin, UpdateView ):
    model         = get_user_model()
    template_name = 'customer_create.html'
    form_class    = CustomerCreateForm


    def post( self, request, *args, **kwargs ):

        FORM = request.POST.copy()

        FORM['last_name'] = FORM['last_name'] 
        FORM['location'] = FORM['location'] 

        request.POST = FORM

        return super( CustomerUpdateView,self ).\
                post( request,*args,**kwargs )











