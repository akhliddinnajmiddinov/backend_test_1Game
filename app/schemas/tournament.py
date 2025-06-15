from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List

class TournamentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    max_players: int = Field(..., ge=2, le=100)
    start_at: datetime

class TournamentResponse(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime
    registered_players: int

    model_config = ConfigDict(from_attributes=True)

class PlayerRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

class PlayerResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class TournamentPlayersResponse(BaseModel):
    tournament_id: int
    players: List[PlayerResponse]