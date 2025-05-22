from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from typing import List

def create_event(db: Session, event: EventCreate, user_id: int) -> Event:
    db_event = Event(**event.dict(), owner_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int, user_id: int) -> Event:
    return db.query(Event).filter(Event.id == event_id, Event.owner_id == user_id).first()

def get_events(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Event]:
    return db.query(Event).filter(Event.owner_id == user_id).offset(skip).limit(limit).all()

def update_event(db: Session, db_event: Event, updates: EventUpdate) -> Event:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, db_event: Event):
    db.delete(db_event)
    db.commit()
