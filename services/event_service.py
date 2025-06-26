from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException, status
from datetime import datetime
import pytz

def create_event(db: Session, event: schemas.EventCreate):
    # Check for duplicate event
    duplicate = db.query(models.Event).filter(
        models.Event.name == event.name,
        models.Event.location == event.location,
        models.Event.start_time == event.start_time,
        models.Event.end_time == event.end_time
    ).first()
    if duplicate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate event entry: An event with the same name, location, and dates already exists.")
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100):
    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    return db.query(models.Event).filter(models.Event.start_time > now_ist).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def register_attendee(db: Session, event_id: int, attendee: schemas.AttendeeCreate):
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if len(db_event.attendees) >= db_event.max_capacity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event at full capacity")

    existing_attendee = db.query(models.Attendee).filter(models.Attendee.event_id == event_id, models.Attendee.email == attendee.email).first()
    if existing_attendee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered for this event")

    db_attendee = models.Attendee(**attendee.dict(), event_id=event_id)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

def get_attendees(db: Session, event_id: int, skip: int = 0, limit: int = 100):
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id).offset(skip).limit(limit).all()
