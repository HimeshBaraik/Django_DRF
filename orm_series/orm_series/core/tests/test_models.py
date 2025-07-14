from django.test import TestCase
from core. models import Restaurant

from datetime import date

class TestRestaurant(TestCase):

    # every single test method that we will write will now have access to self.product and that means 
    # we can share this objects between tests
    def setUp(self):
        self.restaurant = Restaurant(
        name="The Italian Bistro",
        website="http://www.italianbistro.com",
        date_opened=date(2022, 10, 26), 
        latitude=40.7128,             
        longitude=-74.0060,            
        restaurant_type=Restaurant.TypeChoices.ITALIAN  
        )
        
    def test_name_field(self):
        self.assertEqual(self.restaurant.name, "The Italian Bistro")

