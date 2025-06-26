from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from services import event_service
from models import schemas

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return event_service.create_event(db=db, event=event)

@router.get("/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = event_service.get_events(db, skip=skip, limit=limit)
    return events

@router.get("/{event_id}", response_model=schemas.EventWithAttendees)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = event_service.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.post("/{event_id}/register", response_model=schemas.Attendee)
def register_for_event(event_id: int, attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    return event_service.register_attendee(db=db, event_id=event_id, attendee=attendee)

@router.get("/{event_id}/attendees", response_model=List[schemas.Attendee])
def read_event_attendees(event_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attendees = event_service.get_attendees(db=db, event_id=event_id, skip=skip, limit=limit)
    return attendees
