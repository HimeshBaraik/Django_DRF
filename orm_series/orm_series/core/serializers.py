from rest_framework import serializers

# import models
from . models import Restaurant, Sale, Rating, Staff

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(many=True, read_only=True)  # Nested Restaurant Serializer

    class Meta:
        model = Staff
        fields = ['id', 'name', 'restaurant']  # Include restaurant field in StaffSerializer




# serializers are used to handle the validation of incoming data before 
# it's saved to the database. You can perform similar validations in DRF 
# serializers as you do in Django models, but serializers allow for more 
# flexibility when working with API requests.