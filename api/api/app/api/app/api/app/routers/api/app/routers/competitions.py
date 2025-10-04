from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import get_session
from ..models import Player, Season, Match, Appearance

router = APIRouter()

@router.get("/{competition_id}/leaders")
def competition_leaders(competition_id: int, db: Session = Depends(get_session)):
    def minutes(a: Appearance):
        start = 0 if a.started else (a.sub_on_minute or 90)
        end = a.sub_off_minute or 90
        base = max(min(end, 90) - start, 0)
        et = a.extra_time_minutes or 0
        return base + et

    q = db.execute(
        select(Appearance, Match, Season, Player)
        .join(Match, Match.id == Appearance.match_id)
        .join(Season, Season.id == Match.season_id)
        .join(Player, Player.id == Appearance.player_id)
        .where(Season.competition_id == competition_id, Match.status == "played")
    ).all()

    agg: dict[int, dict] = {}
    for row in q:
        a, m, s, p = row
        entry = agg.setdefault(p.id, {"player_id": p.id, "player": p.full_name, "minutes_total": 0})
        entry["minutes_total"] += minutes(a)

    leaders = sorted(agg.values(), key=lambda x: x["minutes_total"], reverse=True)[:50]
    return leaders
