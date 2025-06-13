from pydantic import BaseModel, EmailStr, Field
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

    class Config:
        orm_mode = True

class PlayerRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr

class PlayerResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class TournamentPlayersResponse(BaseModel):
    tournament_id: int
    players: List[PlayerResponse]