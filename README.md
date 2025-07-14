# 🏪 Restaurant API

A RESTful API to manage restaurants, sales, ratings, and staff—with secure JWT authentication.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Models & Relationships](#models--relationships)
- [Authentication Endpoints](#authentication-endpoints)
- [Public Endpoints](#public-endpoints)
- [Protected Endpoints](#protected-endpoints)
- [Usage Examples](#usage-examples)
- [Run](#Running-the-Django-Project)

---

## Overview
The Restaurant API provides CRUD-like access to restaurant data, including sales, ratings, and staff—secured via JWT.

## Features
- User registration, login, logout
- View user profile
- List and add restaurants
- Record/view sales
- Submit/view ratings
- Manage many-to-many staff–restaurant associations  
- Pagination for large datasets

---

## Models & Relationships
- **Restaurant**: `name`, `restaurant_type`, `platform`, `average_rating`, …
- **Rating**: `user`, `restaurant`, `rating (1–5)`
- **Sale**: links to restaurants with `income`, `datetime`
- **Staff**: many-to-many link with restaurants

---

## Authentication Endpoints

| Method | Endpoint           | Description                       |
|--------|--------------------|-----------------------------------|
| POST   | `/auth/register/`  | Register a new user              |
| POST   | `/auth/login/`     | Obtain JWT access & refresh tokens |
| POST   | `/auth/logout/`    | Blacklist refresh token          |
| GET    | `/auth/profile/`   | Fetch authenticated user profile |

---

## Public Endpoints

| Method | Endpoint                                  | Description                                  |
|--------|-------------------------------------------|----------------------------------------------|
| GET    | `/core/`                                  | Homepage with available URLs                 |
| GET    | `/core/allrestaurants`                    | List restaurants (filterable & paginated)    |
| GET    | `/core/allrestaurantsbytype?type={type}` | Filter restaurants by type                   |
| GET    | `/core/counttotalrestaurants`            | Total restaurant count                       |
| GET    | `/core/staff/{staff_id}/restaurants/`    | Restaurants linked to a staff member         |
| GET    | `/core/restaurant/{restaurant_id}/staff/`| Staff linked to a specific restaurant        |

---

## Protected Endpoints *(require JWT access token)*

| Method | Endpoint                  | Description                             |
|--------|---------------------------|-----------------------------------------|
| GET    | `/core/allsales/`         | List all restaurant sales records       |
| GET    | `/core/allratings/`       | View all user ratings                   |
| POST   | `/core/submitrating/`     | Submit rating (`restaurant_id`, `rating`) |
| GET    | `/core/myratings/`        | View logged-in user’s ratings          |
| POST   | `/core/restaurants/add/`  | Add a new restaurant                   |

---

## Usage Examples


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


## 🚀 Running the Django Project

1. Navigate to the project root:
    ```bash
    cd orm_series/orm_series
    ```

2. Start the Django development server:
    ```bash
    python manage.py runserver
    ```


