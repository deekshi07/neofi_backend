from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_event(db, event, current_user.id)

@router.get("/", response_model=list[schemas.EventOut])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_events(db, current_user.id, skip, limit)

@router.get("/{event_id}", response_model=schemas.EventOut)
def read_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = crud.get_event(db, event_id, current_user.id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=schemas.EventOut)
def update_event(event_id: int, event_data: schemas.EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_event = crud.get_event(db, event_id, current_user.id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.update_event(db, db_event, event_data)

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_event = crud.get_event(db, event_id, current_user.id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    crud.delete_event(db, db_event)
    return {"detail": "Event deleted"}
