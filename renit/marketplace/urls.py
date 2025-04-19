from django.urls import path
from .views import (
    ItemListCreate, BookingListCreate, CategoryListCreate, UserSignupView,
    ItemDetail, BookingDetail, CreateCheckoutSession, ReviewListCreate, MessageListCreate
)

urlpatterns = [
    path('items/', ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('bookings/', BookingListCreate.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('reviews/', ReviewListCreate.as_view(), name='review-list-create'),
    path('messages/', MessageListCreate.as_view(), name='message-list-create'),
]