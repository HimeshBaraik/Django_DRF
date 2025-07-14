from drf_yasg import openapi

restaurant_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Restaurant ID"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the restaurant"),
        "website": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Website URL"),
        "date_opened": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description="Date the restaurant opened"),
        "latitude": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Latitude coordinate"),
        "longitude": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description="Longitude coordinate"),
        "restaurant_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=['IN', 'CH', 'IT', 'GR', 'MX', 'FF', 'OT'],
            description="Restaurant type (IN=Indian, CH=Chinese, IT=Italian, etc.)"
        ),
    },
    required=["id", "name", "website", "date_opened", "latitude", "longitude", "restaurant_type"],
    example={
        "id": 1,
        "name": "Spice Heaven",
        "website": "http://spiceheaven.example.com",
        "date_opened": "2023-04-15",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "restaurant_type": "IN"
    }
)
