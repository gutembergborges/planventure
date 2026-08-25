# PlanVenture API

PlanVenture API is the backend service for the PlanVenture travel planning application. It provides authentication, trip management, itinerary generation, user account handling, and secure access to protected endpoints using JWT tokens.

The API is built with Python and Flask, and it uses SQLAlchemy for database persistence.

---

## Features

- User registration and login
- JWT-based authentication
- Protected routes for authenticated users
- Trip creation, retrieval, update, and deletion
- Default itinerary generation based on trip dates and destination
- CORS support for frontend development
- SQLite database by default

---

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Python-dotenv
- SQLite

---

## Project Structure

```text
planventure-api/
├── app.py
├── init_db.py
├── requirements.txt
├── PROMPTS.md
├── instance/
├── middleware/
│   └── auth.py
├── models/
│   ├── __init__.py
│   ├── trip.py
│   └── user.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── trips.py
├── scripts/
│   └── create_db.py
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── itinerary.py
│   ├── parsers.py
│   ├── password.py
│   └── validators.py
└── .env
```

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///planventure.db
JWT_SECRET=your-super-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

You can customize the allowed origins depending on your frontend setup.

---

## Running the Application

From the project folder:

```bash
python app.py
```

The app will run in debug mode by default:

```text
http://localhost:5000
```

---

## API Endpoints

### Health Check

#### GET /health

Returns service health status.

Example response:

```json
{
  "status": "healthy"
}
```

---

### Authentication Routes

#### POST /auth/register

Registers a new user.

Request body:

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

Expected response:

```json
{
  "message": "User registered successfully"
}
```

or

```json
{
  "error": "User already exists"
}
```

---

#### POST /auth/login

Authenticates an existing user and returns a JWT token.

Request body:

```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

Expected response:

```json
{
  "access_token": "<jwt_token>",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

---

### Protected Trip Routes

All trip routes require a valid JWT token in the Authorization header.

Example:

```http
Authorization: Bearer <your_token>
```

---

#### GET /api/trips

Returns all trips for the authenticated user.

Example response:

```json
[
  {
    "id": 1,
    "user_id": 1,
    "destination": "Paris",
    "start_date": "2026-08-20T00:00:00",
    "end_date": "2026-08-27T00:00:00",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "itinerary": [
      {
        "day": 1,
        "title": "Arrival and city walk",
        "description": "Explore the city center"
      }
    ]
  }
]
```

---

#### POST /api/trips

Creates a new trip for the authenticated user.

Request body:

```json
{
  "destination": "Paris",
  "start_date": "2026-08-20T00:00:00",
  "end_date": "2026-08-27T00:00:00",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "itinerary": [
    {
      "day": 1,
      "title": "Arrival and city walk",
      "description": "Explore the city center"
    }
  ]
}
```

Expected response:

```json
{
  "id": 1,
  "user_id": 1,
  "destination": "Paris",
  "start_date": "2026-08-20T00:00:00",
  "end_date": "2026-08-27T00:00:00",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "itinerary": [
    {
      "day": 1,
      "title": "Arrival and city walk",
      "description": "Explore the city center"
    }
  ]
}
```

---

#### GET /api/trips/<trip_id>

Returns details for a single trip belonging to the authenticated user.

---

#### PUT /api/trips/<trip_id>

Updates an existing trip.

Example:

```json
{
  "destination": "Rome",
  "end_date": "2026-09-05T00:00:00"
}
```

---

#### PATCH /api/trips/<trip_id>

Partially updates an existing trip.

---

#### DELETE /api/trips/<trip_id>

Deletes a trip for the authenticated user.

Expected response:

```json
{
  "message": "Trip deleted successfully"
}
```

---

## Authentication

The app uses JSON Web Tokens (JWT) via Flask-JWT-Extended.

### Login flow

1. User sends email and password to `/auth/login`
2. Server validates credentials
3. Server returns a JWT access token
4. Client includes token in `Authorization: Bearer ...` header for protected requests

### Token security

- Tokens are signed with the secret stored in `JWT_SECRET`
- Expiration is set to 1 hour by default
- Unauthorized requests return JSON error responses

---

## Database

By default, the app uses SQLite:

```text
sqlite:///planventure.db
```

This file is created automatically when the app initializes and the database is set up.

You can initialize the database using the project setup scripts or by running the app with the database models imported.

---

## Models

### User Model

Stores user account information such as:

- username
- email
- password hash
- created_at

### Trip Model

Stores itinerary and trip information such as:

- user_id
- destination
- start_date
- end_date
- latitude
- longitude
- itinerary

---

## Middleware

The app includes a custom authentication middleware in:

```text
middleware/auth.py
```

This middleware verifies that:

- a JWT exists
- it is valid
- the user still exists in the database

If validation fails, the API returns:

```json
{
  "error": "Invalid or missing token"
}
```

---

## Error Handling

The API returns consistent JSON responses for common errors:

- 400: Bad request / invalid input
- 401: Unauthorized / invalid or missing token
- 404: Resource not found
- 405: Method not allowed
- 500: Internal server error

Example:

```json
{
  "error": "Missing required fields"
}
```

---

## CORS Configuration

The API allows requests from frontend origins configured in `CORS_ORIGINS`, such as:

```text
http://localhost:3000
http://localhost:5173
```

This enables local frontend development without browser blocking issues.

---

## Notes

- This project is intended for local development and learning.
- In production, you should:
  - use a stronger secret key
  - move from SQLite to PostgreSQL or MySQL
  - use environment-safe configuration
  - enable stricter validation and logging
  - secure session/token management

---

## License

This project is distributed under the project license included in the repository.

---

## Useful Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Check health:

```bash
curl http://localhost:5000/health
```

---

## Example Request

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

---

## Conclusion

PlanVenture API is a lightweight Flask backend designed to support trip planning and user authentication for a travel application. It offers the core features needed to manage users and trip records while remaining easy to extend for future enhancements such as recommendations, weather integration, maps, and itinerary optimization.

```

If you want, I can also turn this into:
- a shorter GitHub-style README,
- a more polished production README,
- or a version tailored specifically for your project’s exact endpoints and behavior.If you want, I can also turn this into:
- a shorter GitHub-style README,
- a more polished production README,
- or a version tailored specifically for your project’s exact endpoints and behavior.