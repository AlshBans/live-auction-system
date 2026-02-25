from django.urls import path
from .views import index, place_bid, view_auctions, view_bids, add_auction, update_auction_priority, view_auctions, close_auction, pay_now, payment_confirmation
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('place_bid/<int:auction_id>/', place_bid, name='place_bid'),
    path('view_bids/<int:auction_id>/', view_bids, name='view_bids'),
    path('add_auction/', add_auction, name='add_auction'),
    path('auctions/', view_auctions, name='view_auctions'),  # URL for viewing auctions
     path('update_priority/<int:auction_id>/', update_auction_priority, name='update_auction_priority'),
         path('close_auction/<int:auction_id>/', close_auction, name='close_auction'),
         path('pay_now/<int:auction_id>/', pay_now, name='pay_now'),
          path('payment_confirmation/<int:auction_id>/', payment_confirmation, name='payment_confirmation'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
