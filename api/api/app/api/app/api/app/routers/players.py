from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import get_session
from ..models import Player, Season, Match, Appearance

router = APIRouter()

@router.get("/search")
def search_players(q: str, db: Session = Depends(get_session)):
    ql = f"%{q.lower()}%"
    res = db.execute(
        select(Player.id, Player.full_name, Player.known_as, Player.nationality)
        .where((Player.full_name.ilike(ql)) | (Player.known_as.ilike(ql)))
        .limit(50)
    ).all()
    return [dict(r._mapping) for r in res]

@router.get("/{player_id}/minutes")
def player_minutes(player_id: int, season_label: str | None = None, db: Session = Depends(get_session)):
    # pega appearances e soma minutos na mão (MVP)
    def minutes(a: Appearance):
        start = 0 if a.started else (a.sub_on_minute or 90)
        end = a.sub_off_minute or 90
        base = max(min(end, 90) - start, 0)
        et = a.extra_time_minutes or 0
        return base + et

    q = db.execute(
        select(Appearance, Match, Season)
        .join(Match, Match.id == Appearance.match_id)
        .join(Season, Season.id == Match.season_id)
        .where(Appearance.player_id == player_id, Match.status == "played")
    ).all()

    agg: dict[str, int] = {}
    for row in q:
        a: Appearance = row[0]
        s: Season = row[2]
        if season_label and s.season_label != season_label:
            continue
        agg[s.season_label] = agg.get(s.season_label, 0) + minutes(a)

    if season_label:
        return {"player_id": player_id, "season": season_label, "minutes_total": agg.get(season_label, 0)}
    return {"player_id": player_id, "seasons": [{"season": k, "minutes_total": v} for k, v in sorted(agg.items())]}
