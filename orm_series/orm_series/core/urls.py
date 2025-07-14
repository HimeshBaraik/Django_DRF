# core/urls.py

from django.urls import path

# importing views
from .views import (
    HomeView, 
    ListAllRestaurants, 
    ListAllSales, 
    ListAllRatings, 
    ListAllRestaurantsOfGivenType,
    CountTotalRestaurants,
    StaffRestaurantListView, 
    RestaurantStaffListView,
    AddRestaurant,
    )

from rest_framework import permissions



urlpatterns = [
    path('', HomeView.as_view(), name='core-home'),
    path('allrestaurants', ListAllRestaurants.as_view()),
    path('allrestaurantsbytype', ListAllRestaurantsOfGivenType.as_view()),
    path('allsales', ListAllSales.as_view()),
    path('allratings', ListAllRatings.as_view()),
    path('counttotalrestaurants', CountTotalRestaurants.as_view()),

    # Many to Many Relationship
    path('staff/<int:pk>/restaurants/', StaffRestaurantListView.as_view(), name='staff-restaurants'),
    path('restaurant/<int:pk>/staff/', RestaurantStaffListView.as_view(), name='restaurant-staff'),

    path('restaurants/add/', AddRestaurant.as_view(), name='add-restaurant'),
]