from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas


def list_contestants(db: Session) -> List[models.Contestant]:
    return list(db.execute(select(models.Contestant).order_by(models.Contestant.name)).scalars())


def get_contestant_by_id(db: Session, contestant_id: int) -> Optional[models.Contestant]:
    return db.get(models.Contestant, contestant_id)


def create_contestant(db: Session, contestant: schemas.ContestantCreate) -> models.Contestant:
    obj = models.Contestant(name=contestant.name.strip(), bio=(contestant.bio or "").strip() or None)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_submission(db: Session, submission: schemas.SubmissionCreate) -> models.Submission:
    obj = models.Submission(
        display_name=submission.display_name.strip(),
        email=(submission.email or None),
        picks=submission.picks,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_submissions(db: Session) -> List[models.Submission]:
    return list(db.execute(select(models.Submission).order_by(models.Submission.created_at.desc())).scalars())
