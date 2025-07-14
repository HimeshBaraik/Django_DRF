from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import the models:
from .models import Restaurant, Sale, Rating, Staff

# import serializers:
from .serializers import RestaurantSerializer, SaleSerializer, RatingSerializer, StaffSerializer

# drf-spectacular:
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

# Authentication
from rest_framework.permissions import IsAuthenticated

# Pagination:
from rest_framework.pagination import PageNumberPagination


# related to core home:
class HomeView(APIView):
    """
    API View for the core app homepage.
    """
    @extend_schema(
        summary="Core app homepage",
        description="Returns a welcome message and list of available API endpoints.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "available_urls": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                },
            }
        },
        tags=["core"]
    )
    def get(self, request):
        accessible_urls = [
            "/allrestaurants",
            "/allrestaurantsbytype",
            "/allsales",
            "/allratings",
            "/counttotalrestaurants",
            "/staff/<int:pk>/restaurants/",
            "/restaurant/<int:pk>/staff/",
            "restaurants/add/",
        ]
        return Response({
            "message": "Welcome to the core app homepage! Here are the available API endpoints:",
            "available_urls": accessible_urls
        }, status=status.HTTP_200_OK)


# Restaurant related:
class ListAllRestaurants(APIView):
    """
    List all restaurants with optional filtering and pagination.
    """
    @extend_schema(
        summary="List all restaurants",
        description="Retrieves a paginated list of all restaurants. Supports filtering by type and platform.",
        responses={200: RestaurantSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="type", type=str, required=False, description="Filter by restaurant type"),
            OpenApiParameter(name="platform", type=str, required=False, description="Filter by platform"),
        ],
        examples=[
            OpenApiExample(
                "Success Response Example",
                value=[
                    {"id": 1, "name": "Pizza Palace", "type": "Italian", "platform": "UberEats"},
                    {"id": 2, "name": "Sushi Spot", "type": "Japanese", "platform": "DoorDash"},
                ],
                response_only=True,
            )
        ],
        tags=["Restaurants"]
    )
    def get(self, request):
        queryset = Restaurant.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = RestaurantSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class ListAllRestaurantsOfGivenType(APIView):
    """
    List restaurants filtered by a specific type.
    """
    @extend_schema(
        summary="List restaurants by type",
        description="Returns all restaurants filtered by the given restaurant type.",
        parameters=[
            OpenApiParameter(
                name="type",
                description="Restaurant type code (e.g. IN, CH, IT, etc.)",
                required=True,
                type=str,
            ),
        ],
        responses={200: RestaurantSerializer(many=True)},
        tags=["Restaurants"]
    )
    def get(self, request):
        type_code = request.query_params.get("type")
        if not type_code:
            return Response({"error": "Query parameter 'type' is required."}, status=status.HTTP_400_BAD_REQUEST)
        restaurants = Restaurant.objects.filter(restaurant_type=type_code)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


class CountTotalRestaurants(APIView):
    """
    Count the total number of restaurants.
    """
    @extend_schema(
        summary="Count total restaurants",
        description="Returns the total number of restaurants in the database.",
        responses={200: int},
        tags=["Restaurants"]
    )
    def get(self, request):
        return Response(Restaurant.objects.count())


class AddRestaurant(APIView):
    """
    Add a new restaurant record.
    """
    @extend_schema(
        summary="Add a new restaurant",
        description="Creates a new restaurant record in the database.",
        request=RestaurantSerializer,
        responses={
            201: RestaurantSerializer,
            400: {"description": "Bad Request - Invalid data provided"},
        },
        examples=[
            OpenApiExample(
                "Example Request Body",
                value={
                    "name": "New Burger Joint",
                    "restaurant_type": "American",
                    "platform": "DoorDash"
                },
                request_only=True,
                media_type="application/json"
            ),
            OpenApiExample(
                "Success Response Example",
                value={
                    "id": 3,
                    "name": "New Burger Joint",
                    "restaurant_type": "American",
                    "platform": "DoorDash",
                    "average_rating": 0.0
                },
                response_only=True,
                media_type="application/json"
            ),
        ],
        tags=["Restaurants"]
    )
    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Sale related:
class ListAllSales(APIView):
    """
    List all sales records.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all sales",
        description="Retrieves all sales transactions recorded in the system. Authentication required.",
        responses={200: SaleSerializer(many=True)},
        tags=["Sales"]
    )
    def get(self, request):
        queryset = Sale.objects.all()
        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)


class ListAllRatings(APIView):
    """
    List all customer ratings.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all ratings",
        description="Retrieves all customer ratings. Authentication required.",
        responses={200: RatingSerializer(many=True)},
        tags=["Ratings"]
    )
    def get(self, request):
        queryset = Rating.objects.all()
        serializer = RatingSerializer(queryset, many=True)
        return Response(serializer.data)


class SubmitRating(APIView):
    """
    Submit a new customer rating for a restaurant.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Submit a rating",
        description="Allows authenticated users to submit a rating for a restaurant.",
        request={
            "type": "object",
            "properties": {
                "restaurant_id": {"type": "integer"},
                "rating": {"type": "number", "format": "float"},
            },
            "required": ["restaurant_id", "rating"],
        },
        responses={
            200: {"type": "object", "properties": {"message": {"type": "string"}}},
            400: {"description": "Missing data"},
            404: {"description": "Invalid restaurant"},
        },
        examples=[
            OpenApiExample(
                "Request Example",
                value={"restaurant_id": 1, "rating": 4.5},
                request_only=True,
                media_type="application/json"
            ),
            OpenApiExample(
                "Success Response Example",
                value={"message": "Rating submitted successfully"},
                response_only=True,
                media_type="application/json"
            ),
        ],
        tags=["Ratings"]
    )
    def post(self, request):
        restaurant_id = request.data.get("restaurant_id")
        rating_value = request.data.get("rating")

        if not (restaurant_id and rating_value):
            return Response({"error": "Missing data"}, status=400)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Invalid restaurant"}, status=404)

        rating = Rating.objects.create(user=request.user, restaurant=restaurant, rating=rating_value)
        return Response({"message": "Rating submitted successfully"})


class MyRatings(APIView):
    """
    List all ratings submitted by the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get my ratings",
        description="Returns all ratings submitted by the authenticated user.",
        responses={200: RatingSerializer(many=True)},
        tags=["Ratings"]
    )
    def get(self, request):
        ratings = Rating.objects.filter(user=request.user)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)


# Staff related:
class StaffRestaurantListView(APIView):
    """
    List all restaurants associated with a specific staff member.
    """
    @extend_schema(
        summary="List restaurants by staff",
        description="Retrieve restaurants associated with a staff member identified by pk.",
        responses={200: RestaurantSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="pk", description="Staff member ID", required=True, type=int),
        ],
        tags=["Staff"]
    )
    def get(self, request, pk):
        try:
            staff = Staff.objects.get(id=pk)
        except Staff.DoesNotExist:
            return Response({"error": "Staff member not found"}, status=status.HTTP_404_NOT_FOUND)

        staff_restaurants = staff.restaurant.all()
        serializer = RestaurantSerializer(staff_restaurants, many=True)
        return Response(serializer.data)


class RestaurantStaffListView(APIView):
    """
    List all staff members associated with a specific restaurant.
    """
    @extend_schema(
        summary="List staff by restaurant",
        description="Retrieve staff members associated with a restaurant identified by pk.",
        responses={200: StaffSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="pk", description="Restaurant ID", required=True, type=int),
        ],
        tags=["Staff"]
    )
    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        restaurant_staff = restaurant.staff_set.all()
        serializer = StaffSerializer(restaurant_staff, many=True)
        return Response(serializer.data)
