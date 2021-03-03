from django.db              import models
from django.urls            import reverse


class Dates( models.Model ):
    '''Removes the duplicated dates in data & help us in filtering.'''

    entry_date    = models.DateField()

    class Meta:
        verbose_name        = 'Date'
        verbose_name_plural = 'Dates'

    def __str__( self ):
        return str( self.entry_date )


class Icecream( models.Model ):
    '''Icecream registration, these property remains static forever.'''

    CATEGORIES = ( 
                   ('Cup',  'Cup Type'),
                   ('Cone', 'Cone Type'),
                   ('Candy-Bar', 'Candy Bar Type'),
                   ('Choco-Bar', 'Choco Bar Type'),
                 )
    
    flavour_name    = models.CharField( max_length=30 )
    per_piece_price = models.PositiveSmallIntegerField()
    per_box_pieces  = models.PositiveSmallIntegerField()
    category        = models.CharField( choices=CATEGORIES, max_length=15 )
  

    @property
    def per_box_price( self ):
        return self.per_piece_price * self.per_box_pieces
 
    
    def save( self, *args, **kwargs ):
        '''Flavour name should be title case'''

        self.flavour_name = self.flavour_name.title()
        
        '''
        Create Total model with new icecream
        where we calculate total_boxes
        '''

        super( Icecream, self ).save( *args, **kwargs )


    def __str__( self ):
        return '{} ({}nos x {}rs)'.format( 
                                         self.flavour_name, 
                                         self.per_box_pieces,
                                         self.per_piece_price
                                        )


class Total( models.Model ):
    '''Current overall stock reports'''
    icecream       = models.OneToOneField( Icecream, on_delete=models.PROTECT )
    total_boxes    = models.PositiveSmallIntegerField( default=0 )
    
    class Meta:
        verbose_name        = 'Total Stock'
        verbose_name_plural = 'Total Stocks'


    @property
    def current_boxes_price( self ):
        '''Current stock price,how much price of stock we have'''

        return self.icecream.per_box_price * self.total_boxes

    
    def __str__( self ):
        '''Returns the OneToOne Icecream fields.'''

        return '{} {} ({} Left)'.format( 
                                      self.icecream.flavour_name,
                                      self.icecream.category,
                                      self.total_boxes
                                   )


class Stock( models.Model ):
    '''Data as per date only,like how much quantity comes in that date.'''

    total         = models.ForeignKey( Total, on_delete=models.PROTECT )

    # Add Stock
    current_boxes = models.PositiveSmallIntegerField( default=0 )
    arrival_boxes = models.PositiveSmallIntegerField( default=0 )
    all_boxes     = models.PositiveSmallIntegerField( default=0 )
    
    # Supply Stock
    sold_boxes    = models.PositiveSmallIntegerField( default=0 )
    remain_boxes  = models.PositiveSmallIntegerField( default=0 )

    entry_date    = models.ForeignKey( Dates,on_delete=models.PROTECT )


    @property
    def todays_sale( self ):
        '''Per box price x total boxes sold'''

        return self.total.icecream.per_box_price * self.sold_boxes
   

    def get_absolute_url( self ):
        '''We will redirect to that Date in which stock is created.'''

        return reverse('current_stock')#,args=[ str(self.entry_date.id) ] )


    def save( self, *args, **kwargs ):
        '''Flavour name should be title case'''

        self.all_boxes = self.current_boxes + self.arrival_boxes
        
        if self.arrival_boxes == 0:
            self.all_boxes = self.current_boxes 

        if self.sold_boxes == 0:
            self.remain_boxes = self.all_boxes

        super( Stock, self ).save( *args, **kwargs )


    def __str__( self ):
        return '{} - {}'.format( 
                          self.entry_date.entry_date,
                          self.total.icecream.flavour_name
                        )


