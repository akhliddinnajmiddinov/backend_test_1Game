from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.tournament import TournamentRepository
from app.schemas.tournament import TournamentCreate, TournamentResponse, PlayerRegister, PlayerResponse, TournamentPlayersResponse
from typing import List

class TournamentService:
    def __init__(self, db: Session):
        self.repo = TournamentRepository(db)

    async def create_tournament(self, tournament: TournamentCreate) -> TournamentResponse:
        if tournament.max_players < 2:
            raise HTTPException(status_code=422, detail="Maximum players must be at least 2")
        db_tournament = await self.repo.create_tournament(tournament)
        return TournamentResponse(
            id=db_tournament.id,
            name=db_tournament.name,
            max_players=db_tournament.max_players,
            start_at=db_tournament.start_at,
            registered_players=0
        )

    async def register_player(self, tournament_id: int, player: PlayerRegister) -> PlayerResponse:
        # Check if tournament exists
        db_tournament = await self.repo.get_tournament(tournament_id)
        if not db_tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")

        # Check player count
        player_count = await self.repo.get_player_count(tournament_id)
        if player_count >= db_tournament.max_players:
            raise HTTPException(status_code=400, detail="Tournament is full")

        # Check for duplicate email
        existing_player = await self.repo.get_player_by_email(tournament_id, player.email)
        if existing_player:
            raise HTTPException(status_code=400, detail="Email already registered in this tournament")

        # Register player
        db_player = await self.repo.register_player(tournament_id, player)
        return PlayerResponse(
            id=db_player.id,
            name=db_player.name,
            email=db_player.email
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