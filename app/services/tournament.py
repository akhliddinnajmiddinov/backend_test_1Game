from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.tournament import TournamentRepository
from app.schemas.tournament import TournamentCreate, TournamentResponse, PlayerRegister, PlayerResponse, TournamentPlayersResponse
from typing import List
from datetime import datetime, timezone

class TournamentService:
    def __init__(self, db: Session):
        self.repo = TournamentRepository(db)

    async def create_tournament(self, tournament: TournamentCreate) -> TournamentResponse:
        # Check if tournament exists with this name
        existing_tournament = await self.repo.get_tournament_by_name(tournament.name)
        if existing_tournament:
            raise HTTPException(status_code=400, detail="There is tournament with this name already!")
        
        # Check if tournament's start_time is 
        if tournament.start_at <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Tournament can't start in the past")
        
        db_tournament = await self.repo.create_tournament(tournament)
        return TournamentResponse(
            id=db_tournament.id,
            name=db_tournament.name,
            max_players=db_tournament.max_players,
            start_at=db_tournament.start_at,
            registered_players=db_tournament.player_count
        )

    async def get_tournament(self, tournament_id: int) -> TournamentResponse:
        # Check if tournament exists with this name
        db_tournament = await self.repo.get_tournament(tournament_id)
        if not db_tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")
        return TournamentResponse(
            id=db_tournament.id,
            name=db_tournament.name,
            max_players=db_tournament.max_players,
            start_at=db_tournament.start_at,
            registered_players=db_tournament.player_count
        )

    async def get_all_tournaments(self) -> List[TournamentResponse]:
        # Check if tournament exists with this name
        db_tournaments = await self.repo.get_all_tournaments()
        return [
            TournamentResponse(
                id=db_tournament.id,
                name=db_tournament.name,
                max_players=db_tournament.max_players,
                start_at=db_tournament.start_at,
                registered_players=db_tournament.player_count
            )
            for db_tournament in db_tournaments
        ]

    async def register_player(self, tournament_id: int, player: PlayerRegister) -> PlayerResponse:
        # Check if tournament exists
        db_tournament = await self.repo.get_tournament(tournament_id)
        if not db_tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")

        # Check player count
        if db_tournament.player_count >= db_tournament.max_players:
            raise HTTPException(status_code=400, detail="Tournament is full")

        # Check for duplicate email
        existing_player = await self.repo.get_player_by_email(tournament_id, player.email)
        if existing_player:
            raise HTTPException(status_code=400, detail="Email already registered in this tournament")

        # Register player
        db_player = await self.repo.register_player(tournament_id, player)
        return TournamentResponse(
            id=db_tournament.id,
            name=db_tournament.name,
            max_players=db_tournament.max_players,
            start_at=db_tournament.start_at,
            registered_players=db_tournament.player_count
        )

    async def get_tournament_players(self, tournament_id: int) -> TournamentPlayersResponse:
        # Check if tournament exists
        db_tournament = await self.repo.get_tournament(tournament_id)
        if not db_tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")

        # Get players
        players = await self.repo.get_players(tournament_id)
        player_responses = [
            PlayerResponse(id=p.id, name=p.name, email=p.email)
            for p in players
        ]
        return TournamentPlayersResponse(
            tournament_id=tournament_id,
            players=player_responses
        )