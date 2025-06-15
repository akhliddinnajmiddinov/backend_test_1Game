from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.tournament import TournamentCreate, TournamentResponse, PlayerRegister, TournamentPlayersResponse
from app.services.tournament import TournamentService
from typing import List

router = APIRouter()

@router.post("/", response_model=TournamentResponse)
async def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.create_tournament(tournament)

@router.get("/", response_model=List[TournamentResponse])
async def get_all_tournaments(db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.get_all_tournaments()

@router.get("/{tournament_id}/", response_model=TournamentResponse)
async def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.get_tournament(tournament_id)

@router.post("/{tournament_id}/register", response_model=TournamentResponse)
async def register_player(tournament_id: int, player: PlayerRegister, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.register_player(tournament_id, player)

@router.get("/{tournament_id}/players", response_model=TournamentPlayersResponse)
async def get_tournament_players(tournament_id: int, db: Session = Depends(get_db)):
    service = TournamentService(db)
    return await service.get_tournament_players(tournament_id)