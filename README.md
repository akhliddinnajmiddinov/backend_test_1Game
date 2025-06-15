# 🏆 Tournament API

A **FastAPI**-based API for managing tournaments and player registrations, using **SQLAlchemy 2.0**, **PostgreSQL**, **Alembic**, and **Docker**.  
Supports creating tournaments, registering players, and listing players — with asynchronous operations, **Pydantic** validation, and robust error handling.

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd backend_test_1Game
```

### 2. Install Dependencies

Ensure **Docker** and **Docker Compose** are installed on your system.

### 3. Create .env file using .env.example and run the Development Server

```bash
make dev
```

🌐 Access the API at `http://localhost:8000/docs`.

### 4. Run Migrations (Optional)

```bash
make migrate
```

🛠 Initializes the **PostgreSQL** database and applies **Alembic** migrations.

### 5. Run Tests

```bash
make test
```

✅ Executes **Pytest** tests for player registration and other functionality.

### 6. Run Linting

```bash
make lint
```

🔍 Checks code with **Ruff** and **Mypy** for style and type safety.

### 7. View Logs

```bash
make logs
```

📜 Displays real-time logs from the **Docker** containers.

### 8. Stop and Clean Up

```bash
make down
```

🧹 Removes containers and volumes for a fresh setup.

---

## 🌟 API Usage

Interactive documentation is available at `http://localhost:8000/docs`. Key endpoints:

### Create Tournament

```bash
curl -X POST "http://localhost:8000/tournaments/" -H "Content-Type: application/json" -d '{"name": "Weekend Cup", "max_players": 8, "start_at": "2025-06-01T15:00:00Z"}'
```

### Register Player

```bash
curl -X POST "http://localhost:8000/tournaments/1/register" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'
```

### List Players

```bash
curl -X GET "http://localhost:8000/tournaments/1/players"
```

📖 See `API_DOCUMENTATION.md` for full endpoint details.

---
