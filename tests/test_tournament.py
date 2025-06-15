import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timezone, timedelta
from app.main import app
from app.db import Base, get_db
from app.schemas.tournament import TournamentCreate, PlayerRegister
from app.services.tournament import TournamentService
from app.repositories.tournament import TournamentRepository
from app.models.tournament import Tournament, Player

# Test database setup
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

@pytest_asyncio.fixture
async def client():
    return TestClient(app)

@pytest_asyncio.fixture
async def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest_asyncio.fixture
async def tournament_data():
    return TournamentCreate(
        name="Test Tournament",
        max_players=8,
        start_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

@pytest_asyncio.fixture
async def player_data():
    return PlayerRegister(
        name="John Doe",
        email="john@example.com",
    )

@pytest_asyncio.fixture
async def player_data2():
    return PlayerRegister(
        name="Tom Doe",
        email="tom@example.com",
    )

# Router Tests
@pytest.mark.asyncio
async def test_create_tournament(client, tournament_data):
    # Convert datetime to ISO format
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    response = client.post("/tournaments/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == tournament_data.name
    assert response_data["max_players"] == tournament_data.max_players
    assert response_data["registered_players"] == 0

@pytest.mark.asyncio
async def test_create_tournament_duplicate_name(client, tournament_data):
    # Convert datetime to ISO format
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    client.post("/tournaments/", json=data)
    response = client.post("/tournaments/", json=data)
    assert response.status_code == 400
    assert "There is tournament with this name already!" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_tournament_past_start_time(client, tournament_data):
    tournament_data.start_at = datetime.now(timezone.utc) - timedelta(days=1)
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    response = client.post("/tournaments/", json=data)
    assert response.status_code == 400
    assert "Tournament can't start in the past" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_all_tournaments(client, tournament_data):
    # Create a tournament
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    client.post("/tournaments/", json=data)
    response = client.get("/tournaments/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == tournament_data.name

@pytest.mark.asyncio
async def test_get_tournament(client, tournament_data):
    # Create a tournament
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    create_response = client.post("/tournaments/", json=data)
    tournament_id = create_response.json()["id"]
    # Get the tournament
    response = client.get(f"/tournaments/{tournament_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tournament_data.name
    assert data["max_players"] == tournament_data.max_players

@pytest.mark.asyncio
async def test_get_tournament_not_found(client):
    response = client.get("/tournaments/999/")
    assert response.status_code == 404
    assert "Tournament not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_player(client, tournament_data, player_data):
    # Create a tournament
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    create_response = client.post("/tournaments/", json=data)
    tournament_id = create_response.json()["id"]
    # Register a player
    response = client.post(
        f"/tournaments/{tournament_id}/register", json=player_data.model_dump()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["registered_players"] == 1

@pytest.mark.asyncio
async def test_register_player_tournament_full(client, tournament_data, player_data, player_data2):
    # Create a tournament with max_players=1
    tournament_data.max_players = 2
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    create_response = client.post("/tournaments/", json=data)
    print("create_response")
    print(create_response.json())
    tournament_id = create_response.json()["id"]
    # Register first player
    client.post(f"/tournaments/{tournament_id}/register", json=player_data.model_dump())
    client.post(f"/tournaments/{tournament_id}/register", json=player_data2.model_dump())
    # Try to register another player
    response = client.post(
        f"/tournaments/{tournament_id}/register",
        json=PlayerRegister(name="Jane Doe", email="jane@example.com").model_dump(),
    )
    assert response.status_code == 400
    assert "Tournament is full" in response.json()["detail"]

@pytest.mark.asyncio
async def test_register_player_duplicate_email(client, tournament_data, player_data):
    # Create a tournament
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    create_response = client.post("/tournaments/", json=data)
    tournament_id = create_response.json()["id"]
    # Register player
    client.post(f"/tournaments/{tournament_id}/register", json=player_data.model_dump())
    # Try to register same email
    response = client.post(f"/tournaments/{tournament_id}/register", json=player_data.model_dump())
    assert response.status_code == 400
    assert "Email already registered in this tournament" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_tournament_players(client, tournament_data, player_data):
    # Create a tournament
    data = tournament_data.model_dump()
    data["start_at"] = data["start_at"].isoformat()
    create_response = client.post("/tournaments/", json=data)
    tournament_id = create_response.json()["id"]
    # Register a player
    client.post(f"/tournaments/{tournament_id}/register", json=player_data.model_dump())
    # Get players
    response = client.get(f"/tournaments/{tournament_id}/players")
    assert response.status_code == 200
    data = response.json()
    assert data["tournament_id"] == tournament_id
    assert len(data["players"]) == 1
    assert data["players"][0]["email"] == player_data.email