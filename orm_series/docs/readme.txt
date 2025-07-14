Restaurant API — README

Overview
--------
This API manages restaurants, sales, ratings, and staff. It uses JWT authentication for secure access.

Models & Relations
------------------
- Restaurant: name, type, platform, average rating, etc.
- Rating: user ratings for restaurants (1-5).
- Sale: sales records linked to restaurants.
- Staff: staff members linked to many restaurants (many-to-many).

Authentication Endpoints
------------------------
- Register: POST username, password, (email optional). Returns success or error.

  Example Request:
  POST /auth/register/
  {
    "username": "john_doe",
    "password": "strongpassword123",
    "email": "john@example.com"
  }

  Example Response:
  {
    "message": "User created successfully"
  }

- Login: POST username & password. Returns JWT tokens (access & refresh).

  Example Request:
  POST /auth/login/
  {
    "username": "john_doe",
    "password": "strongpassword123"
  }

  Example Response:
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }

- Logout: POST refresh token to blacklist.

  Example Request:
  POST /auth/logout/
  {
    "refresh": "<refresh_token>"
  }

  Example Response:
  HTTP 205 Reset Content (no body)

- Profile: GET user info (username, email, is_staff). Requires auth.

  Example Request:
  GET /auth/profile/
  Headers: Authorization: Bearer <access_token>

  Example Response:
  {
    "username": "john_doe",
    "email": "john@example.com",
    "is_staff": false
  }

Core API Endpoints
------------------

Public (no auth needed):

- Home: GET welcome message + available endpoints list.

  Example Request:
  GET /core/

  Example Response:
  {
    "message": "Welcome to the core app homepage! Here are the available API endpoints:",
    "available_urls": [
      "/allrestaurants",
      "/allrestaurantsbytype",
      "/allsales",
      "/allratings",
      "/counttotalrestaurants",
      "/staff/<int:pk>/restaurants/",
      "/restaurant/<int:pk>/staff/",
      "restaurants/add/"
    ]
  }

- List All Restaurants: GET with optional filters `type`, `platform`. Paginated (10 per page).

  Example Request:
  GET /core/allrestaurants?page=1

  Example Response:
  {
    "count": 25,
    "next": "/core/allrestaurants?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Pizza Palace",
        "restaurant_type": "IT",
        "platform": "UberEats",
        "average_rating": 4.5
      }
    ]
  }

- List Restaurants by Type: GET with required `type` query param.

  Example Request:
  GET /core/allrestaurantsbytype?type=IT

  Example Response:
  [
    {
      "id": 1,
      "name": "Pizza Palace",
      "restaurant_type": "IT",
      "platform": "UberEats",
      "average_rating": 4.5
    }
  ]

- Count Total Restaurants: GET returns count integer.

  Example Request:
  GET /core/counttotalrestaurants

  Example Response:
  25

- List Restaurants by Staff ID: GET restaurants linked to a staff member.

  Example Request:
  GET /core/staff/5/restaurants/

  Example Response:
  [
    {
      "id": 1,
      "name": "Pizza Palace",
      "restaurant_type": "IT",
      "platform": "UberEats",
      "average_rating": 4.5
    }
  ]

- List Staff by Restaurant ID: GET staff linked to a restaurant.

  Example Request:
  GET /core/restaurant/1/staff/

  Example Response:
  [
    {
      "id": 3,
      "name": "Alice"
    },
    {
      "id": 4,
      "name": "Bob"
    }
  ]

Protected (auth required):

- List All Sales: GET all sales.

  Example Request:
  GET /core/allsales/
  Headers: Authorization: Bearer <access_token>

  Example Response:
  [
    {
      "id": 10,
      "restaurant": 1,
      "income": "2500.00",
      "datetime": "2025-07-10T12:00:00Z"
    }
  ]

- List All Ratings: GET all ratings.

  Example Request:
  GET /core/allratings/
  Headers: Authorization: Bearer <access_token>

  Example Response:
  [
    {
      "id": 20,
      "user": 1,
      "restaurant": 1,
      "rating": 5
    }
  ]

- Submit Rating: POST with `restaurant_id` and `rating` (1-5).

  Example Request:
  POST /core/submitrating/
  Headers: Authorization: Bearer <access_token>
  {
    "restaurant_id": 1,
    "rating": 4
  }

  Example Response:
  {
    "message": "Rating submitted successfully"
  }

- List My Ratings: GET ratings by current user.

  Example Request:
  GET /core/myratings/
  Headers: Authorization: Bearer <access_token>

  Example Response:
  [
    {
      "id": 20,
      "user": 1,
      "restaurant": 1,
      "rating": 5
    }
  ]

- Add Restaurant: POST new restaurant data.

  Example Request:
  POST /core/restaurants/add/
  Headers: Authorization: Bearer <access_token>
  {
    "name": "New Burger Joint",
    "restaurant_type": "FF",
    "platform": "DoorDash"
  }

  Example Response:
  {
    "id": 3,
    "name": "New Burger Joint",
    "restaurant_type": "FF",
    "platform": "DoorDash",
    "average_rating": 0.0
  }

API Docs
--------
- Swagger UI: /schema/swagger-ui/
- Redoc: /schema/redoc/
- OpenAPI JSON: /schema/

Notes
-----
- Pagination defaults to 10 items per page on list endpoints.
- Use JWT access token in Authorization header to access protected routes.

