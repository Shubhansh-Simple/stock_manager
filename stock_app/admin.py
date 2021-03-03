from django.contrib import admin
from .models        import Dates,Total,Icecream,Stock

admin.site.register( Icecream )
admin.site.register( Total )
admin.site.register( Dates )
admin.site.register( Stock )

