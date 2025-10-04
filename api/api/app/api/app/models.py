from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, ForeignKey, Boolean, JSON, TIMESTAMP, Text
from .db import Base

class Competition(Base):
    __tablename__ = "competitions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    country: Mapped[str | None] = mapped_column(String, nullable=True)

class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    country: Mapped[str | None] = mapped_column(String, nullable=True)

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(Text)
    known_as: Mapped[str | None] = mapped_column(String, nullable=True)
    dob: Mapped[Date | None] = mapped_column(Date, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String, nullable=True)

class Season(Base):
    __tablename__ = "seasons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    season_label: Mapped[str] = mapped_column(String)

class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    match_date: Mapped[str | None] = mapped_column(TIMESTAMP, nullable=True)
    home_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    minutes_regulation: Mapped[int | None] = mapped_column(Integer, nullable=True, default=90)

class Appearance(Base):
    __tablename__ = "appearances"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    started: Mapped[bool] = mapped_column(Boolean, default=False)
    sub_on_minute: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sub_off_minute: Mapped[int | None] = mapped_column(Integer, nullable=True)
    red_card_minute: Mapped[int | None] = mapped_column(Integer, nullable=True)
    extra_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
