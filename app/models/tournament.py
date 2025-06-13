from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    max_players = Column(Integer, nullable=False)
    start_at = Column(DateTime, nullable=False)

    players = relationship("Player", back_populates="tournament", cascade="all, delete-orphan")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)

    tournament = relationship("Tournament", back_populates="players")

    __table_args__ = (
        UniqueConstraint("email", "tournament_id", name="unique_email_per_tournament"),
    )