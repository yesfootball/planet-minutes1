from fastapi import FastAPI
from .db import Base, engine
from .routers import players, competitions, ops

app = FastAPI(title="Planet Minutes (MVP)")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(competitions.router, prefix="/competitions", tags=["competitions"])
app.include_router(ops.router, prefix="/ops", tags=["ops"])

@app.get("/")
def root():
    return {"ok": True}
