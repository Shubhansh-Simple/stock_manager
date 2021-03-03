from django.contrib.auth.models import AbstractUser
from django.db                  import models
from django.urls                import reverse


class Customer( AbstractUser ):
    location = models.CharField( max_length=200 )

    def get_absolute_url( self ):
        '''We will redirect to that User List after creating/updating'''

        return reverse( 'customer_list' )

