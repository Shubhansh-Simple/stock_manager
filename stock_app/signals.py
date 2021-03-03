from django.db.models.signals import post_save
from django.dispatch          import receiver

from .models                  import Total,Icecream

@receiver( post_save, sender=Icecream )
def create_model( sender, instance, created, **kwargs ):
    if created:
        Total.objects.create( icecream=instance )




