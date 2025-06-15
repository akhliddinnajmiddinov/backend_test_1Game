from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.tournament import Tournament, Player
from app.schemas.tournament import TournamentCreate, PlayerRegister
from typing import Optional, List

class TournamentRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_tournament(self, tournament: TournamentCreate) -> Tournament:
        db_tournament = Tournament(
            name=tournament.name,
            max_players=tournament.max_players,
            start_at=tournament.start_at
        )
        self.db.add(db_tournament)
        self.db.commit()
        self.db.refresh(db_tournament)
        return db_tournament

    async def get_tournament(self, tournament_id: int) -> Optional[Tournament]:
        result = self.db.execute(
            select(Tournament).where(Tournament.id == tournament_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_tournaments(self) -> List[Tournament]:
        result = self.db.execute(select(Tournament))
        return result.scalars().all()

    async def get_tournament_by_name(self, name: str) -> Optional[Tournament]:
        result = self.db.execute(
            select(Tournament).where(Tournament.name == name)
        )
        return result.scalar_one_or_none()

    async def get_player_by_email(self, tournament_id: int, email: str) -> Optional[Player]:
        result = self.db.execute(
            select(Player).where(
                Player.tournament_id == tournament_id,
                Player.email == email
            )
        )
        return result.scalar_one_or_none()

    async def register_player(self, tournament_id: int, player: PlayerRegister) -> Player:
        db_player = Player(
            name=player.name,
            email=player.email,
            tournament_id=tournament_id
        )
        self.db.add(db_player)
        self.db.commit()
        self.db.refresh(db_player)
        return db_player

    async def get_players(self, tournament_id: int) -> List[Player]:
        result = self.db.execute(
            select(Player).where(Player.tournament_id == tournament_id)
        )
        return result.scalars().all()