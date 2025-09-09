import json
import os
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Contestant


DEFAULT_CONTESTANTS: List[str] = [
    "Contestant A",
    "Contestant B",
    "Contestant C",
    "Contestant D",
    "Contestant E",
]


def _read_names_from_file(path: str) -> List[str]:
    if not os.path.exists(path):
        # Create a starter file the user can edit
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONTESTANTS, f, indent=2)
        return DEFAULT_CONTESTANTS
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                names = [str(x).strip() for x in data if str(x).strip()]
                return names
    except Exception:
        pass
    return DEFAULT_CONTESTANTS


def seed_contestants_if_empty(db: Session, path: str) -> int:
    existing_one = db.execute(select(Contestant).limit(1)).scalar_one_or_none()
    if existing_one is not None:
        return 0
    names = _read_names_from_file(path)
    to_create = [Contestant(name=name) for name in names]
    for obj in to_create:
        db.add(obj)
    db.commit()
    return len(to_create)
