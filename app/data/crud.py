"""
CRUD operations over DB.
"""
from sqlalchemy.orm import Session

from data import models


def create_recognition(db: Session, recognition: models.Recognition):
    db.add(recognition)
    db.commit()
    db.refresh(recognition)
    return recognition


def get_recognition(db: Session, recognition_id: int):
    return db.query(models.Recognition).filter(models.Recognition.id == recognition_id).first()


def update_recognition(db: Session, recognition_id: int, updated_data: dict):
    recognition = db.query(models.Recognition).filter(models.Recognition.id == recognition_id).first()
    for key, value in updated_data.items():
        setattr(recognition, key, value)
    db.commit()
    return recognition


def delete_recognition(db: Session, recognition_id: int):
    recognition = db.query(models.Recognition).filter(models.Recognition.id == recognition_id).first()
    db.delete(recognition)
    db.commit()
    return recognition


def get_all_recognitions(db: Session):
    return db.query(models.Recognition).all()
