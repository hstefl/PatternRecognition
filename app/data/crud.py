"""
CRUD operations over DB.
"""
from typing import cast

from sqlalchemy.orm import Session

from data.models import Recognition


def create_recognition(db: Session, recognition: Recognition) -> None:
    db.add(recognition)
    db.commit()
    db.refresh(recognition)


def get_recognition(db: Session, recognition_id: int) -> Recognition | None:
    return db.query(Recognition).filter(Recognition.id == recognition_id).first()


def update_recognition(db: Session, recognition_id: int, updated_data: dict) -> Recognition | None:
    recognition = db.query(Recognition).filter(Recognition.id == recognition_id).first()
    for key, value in updated_data.items():
        setattr(recognition, key, value)
    db.commit()
    return recognition


def delete_recognition(db: Session, recognition_id: int) -> Recognition | None:
    recognition = db.query(Recognition).filter(Recognition.id == recognition_id).first()
    db.delete(recognition)
    db.commit()
    return recognition


def get_all_recognitions(db: Session) -> list[Recognition]:
    result = db.query(Recognition).all()

    # TODO investigate why linter thinks that "Expected type list[Recognition] but got list[Type[Recognition]]"
    return cast(list[Recognition], result)
