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
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Authentication](#authentication)
- [Pagination](#pagination)
- [API Docs](#api-docs)
- [Contributing](#contributing)
- [License](#license)

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

