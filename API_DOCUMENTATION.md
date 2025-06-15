# Tournament API Documentation

This document describes the API endpoints for the mini-tournament system, built with FastAPI, SQLAlchemy 2.0, and PostgreSQL. The API supports creating tournaments, registering players, and listing players, with asynchronous operations, Pydantic validation, and error handling.

## Base URL
`http://localhost:8000`

## Endpoints

### 1. Create a Tournament
- **Method**: POST
- **Path**: `/tournaments/`
- **Description**: Creates a new tournament with a name, maximum number of players, and start date (UTC).
- **Request Body**:
  ```json
  {
      "name": "Weekend Cup",
      "max_players": 8,
      "start_at": "2025-06-01T15:00:00Z"
  }
  ```
  - `name` (string, required): Tournament name.
  - `max_players` (integer, required): Maximum number of players (positive integer).
  - `start_at` (datetime, required): Start date in UTC (ISO 8601 format).
- **Responses**:
  - **200 OK**:
    ```json
    {
        "id": 1,
        "name": "Weekend Cup",
        "max_players": 8,
        "start_at": "2025-06-01T15:00:00Z",
        "registered_players": 0
    }
    ```
  - **422 Unprocessable Entity**: Invalid request body (e.g., missing fields, invalid datetime).
    ```json
    {
        "detail": [
            {
                "loc": ["body", "start_at"],
                "msg": "Invalid datetime format",
                "type": "value_error.datetime"
            }
        ]
    }
    ```
- **Example**:
  ```bash
  curl -X POST "http://localhost:8000/tournaments/" -H "Content-Type: application/json" -d '{"name": "Weekend Cup", "max_players": 8, "start_at": "2025-06-01T15:00:00Z"}'
  ```

### 2. Get All Tournaments
- **Method**: GET
- **Path**: `/tournaments/`
- **Description**: Retrieves a list of all tournaments.
- **Request Parameters**: None
- **Responses**:
  - **200 OK**:
    ```json
    [
        {
            "id": 1,
            "name": "Weekend Cup",
            "max_players": 8,
            "start_at": "2025-06-01T15:00:00Z",
            "registered_players": 2
        },
        {
            "id": 2,
            "name": "Summer Clash",
            "max_players": 16,
            "start_at": "2025-07-01T12:00:00Z",
            "registered_players": 0
        }
    ]
    ```
  - **404 Not Found**: If no tournaments exist (optional, depending on implementation).
    ```json
    {
        "detail": "No tournaments found"
    }
    ```
- **Example**:
  ```bash
  curl -X GET "http://localhost:8000/tournaments/"
  ```

### 3. Get a Tournament
- **Method**: GET
- **Path**: `/tournaments/{tournament_id}/`
- **Description**: Retrieves details of a specific tournament by ID.
- **Path Parameters**:
  - `tournament_id` (integer, required): ID of the tournament.
- **Responses**:
  - **200 OK**:
    ```json
    {
        "id": 1,
        "name": "Weekend Cup",
        "max_players": 8,
        "start_at": "2025-06-01T15:00:00Z",
        "registered_players": 2
    }
    ```
  - **404 Not Found**: If the tournament ID does not exist.
    ```json
    {
        "detail": "Tournament not found"
    }
    ```
- **Example**:
  ```bash
  curl -X GET "http://localhost:8000/tournaments/1/"
  ```

### 4. Register a Player
- **Method**: POST
- **Path**: `/tournaments/{tournament_id}/register`
- **Description**: Registers a player for a tournament with a name and email.
- **Path Parameters**:
  - `tournament_id` (integer, required): ID of the tournament.
- **Request Body**:
  ```json
  {
      "name": "John Doe",
      "email": "john@example.com"
  }
  ```
  - `name` (string, required): Player’s name.
  - `email` (string, required): Player’s email (must be unique per tournament).
- **Responses**:
  - **200 OK**:
    ```json
    {
        "id": 1,
        "name": "Weekend Cup",
        "max_players": 8,
        "start_at": "2025-06-01T15:00:00Z",
        "registered_players": 1
    }
    ```
  - **400 Bad Request**:
    - If the tournament is full:
      ```json
      {
          "detail": "Tournament has reached maximum players"
      }
      ```
    - If the email is already registered:
      ```json
      {
          "detail": "Email already registered for this tournament"
      }
      ```
  - **404 Not Found**: If the tournament ID does not exist.
    ```json
    {
        "detail": "Tournament not found"
    }
    ```
  - **422 Unprocessable Entity**: Invalid request body (e.g., invalid email).
    ```json
    {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "Invalid email format",
                "type": "value_error.email"
            }
        ]
    }
    ```
- **Example**:
  ```bash
  curl -X POST "http://localhost:8000/tournaments/1/register" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'
  ```

### 5. Get Tournament Players
- **Method**: GET
- **Path**: `/tournaments/{tournament_id}/players`
- **Description**: Retrieves a list of players registered for a specific tournament.
- **Path Parameters**:
  - `tournament_id` (integer, required): ID of the tournament.
- **Responses**:
  - **200 OK**:
    ```json
    {
        "tournament_id": 1,
        "players": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com"
            }
        ]
    }
    ```
  - **404 Not Found**: If the tournament ID does not exist.
    ```json
    {
        "detail": "Tournament not found"
    }
    ```
- **Example**:
  ```bash
  curl -X GET "http://localhost:8000/tournaments/1/players"
  ```

## Notes
- All endpoints use asynchronous handlers (`async def`) for performance.
- Pydantic models (`TournamentCreate`, `TournamentResponse`, `PlayerRegister`, `TournamentPlayersResponse`) validate requests and responses.
- Error handling follows HTTP standards (400, 404, 422).
- The API is documented interactively at `http://localhost:8000/docs`.