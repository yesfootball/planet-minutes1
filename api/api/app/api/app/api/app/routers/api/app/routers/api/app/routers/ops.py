from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_session, Base, engine
from ..models import Competition, Season, Team, Player, Match, Appearance

router = APIRouter()

@router.post("/seed")
def seed(db: Session = Depends(get_session)):
    # cria tabelas (idempotente)
    Base.metadata.create_all(bind=engine)

    # dados mínimos
    comp = Competition(name="Demo League", country="Nowhere")
    db.add(comp); db.flush()
    season = Season(competition_id=comp.id, season_label="2025/26")
    db.add(season); db.flush()
    alpha = Team(name="Alpha FC"); beta = Team(name="Beta United")
    db.add_all([alpha, beta]); db.flush()
    joao = Player(full_name="João Silva", known_as="João", nationality="BRA")
    van = Player(full_name="Nguyen Van A", known_as="Van A", nationality="VIE")
    tanaka = Player(full_name="Keisuke Tanaka", known_as="Tanaka", nationality="JPN")
    db.add_all([joao, van, tanaka]); db.flush()
    match = Match(season_id=season.id, match_date="2025-09-10 19:00:00",
                  home_team_id=alpha.id, away_team_id=beta.id, status="played", minutes_regulation=90)
    db.add(match); db.flush()
    db.add_all([
        Appearance(match_id=match.id, player_id=joao.id, team_id=alpha.id, started=True, sub_on_minute=None, sub_off_minute=None, extra_time_minutes=0),
        Appearance(match_id=match.id, player_id=van.id, team_id=beta.id, started=False, sub_on_minute=60, sub_off_minute=None, extra_time_minutes=0),
        Appearance(match_id=match.id, player_id=tanaka.id, team_id=beta.id, started=True, sub_on_minute=None, sub_off_minute=75, extra_time_minutes=0),
    ])
    db.commit()
    return {"ok": True}
