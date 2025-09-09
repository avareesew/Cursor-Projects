import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, get_db, DB_PATH
from . import crud, schemas, models
from .config import MIN_PICKS, DATA_CONTESTANTS_PATH
from .data_loader import seed_contestants_if_empty


def ensure_data_dir():
    data_dir = os.path.dirname(DB_PATH)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)


ensure_data_dir()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DWTS Fantasy Draft API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/contestants", response_model=List[schemas.ContestantOut])
def get_contestants(db: Session = Depends(get_db)):
    return crud.list_contestants(db)


@app.post("/api/contestants", response_model=schemas.ContestantOut)
def post_contestant(payload: schemas.ContestantCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_contestant(db, payload)
    except Exception as exc:  # unique constraint, etc.
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/submissions", response_model=schemas.SubmissionOut)
def post_submission(payload: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    # Validate picks exist
    # enforce unique picks and minimum picks
    if len(payload.picks) < MIN_PICKS:
        raise HTTPException(status_code=400, detail=f"Please select at least {MIN_PICKS} contestants.")
    if len(set(payload.picks)) != len(payload.picks):
        raise HTTPException(status_code=400, detail="Duplicate picks are not allowed.")
    for contestant_id in payload.picks:
        if crud.get_contestant_by_id(db, contestant_id) is None:
            raise HTTPException(status_code=400, detail=f"Invalid contestant id: {contestant_id}")
    return crud.create_submission(db, payload)


@app.get("/api/submissions", response_model=List[schemas.SubmissionOut])
def get_submissions(db: Session = Depends(get_db)):
    return crud.list_submissions(db)


static_dir = "/workspace/static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.on_event("startup")
def on_startup():
    # Seed contestants on first run
    with next(get_db()) as db:
        try:
            seed_contestants_if_empty(db, DATA_CONTESTANTS_PATH)
        except Exception:
            # Ignore seeding errors to avoid blocking app start
            pass
