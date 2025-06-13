from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.tournament import TournamentCreate, TournamentResponse, PlayerRegister, PlayerResponse, TournamentPlayersResponse
from app.services.tournament import TournamentService

router = APIRouter()

@router.post("/", response_model=TournamentResponse)
async def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.create_tournament(tournament)

@router.post("/{tournament_id}/register", response_model=PlayerResponse)
async def register_player(tournament_id: int, player: PlayerRegister, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.register_player(tournament_id, player)

@router.get("/{tournament_id}/players", response_model=TournamentPlayersResponse)
async def get_tournament_players(tournament_id: int, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.get_tournament_players(tournament_id)