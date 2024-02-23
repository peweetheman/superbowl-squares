from django.urls import path
from .views import square_selection, payment_page, success_page

urlpatterns = [
    path('', square_selection, name='square_selection'),  # Updated name
    path('payment_page/', payment_page, name='payment_page'),  # Updated name and added trailing slash for consistency
    path('success_page/', success_page, name='success_page'),  # Updated name and added trailing slash for consistency
]
