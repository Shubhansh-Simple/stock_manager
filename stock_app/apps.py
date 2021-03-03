from django.apps import AppConfig


class StockAppConfig(AppConfig):
    name = 'stock_app'

    def ready( self ):
        import stock_app.signals
