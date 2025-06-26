from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class AttendeeBase(BaseModel):
    name: str
    email: EmailStr


class AttendeeCreate(AttendeeBase):
    pass


class Attendee(AttendeeBase):
    id: int
    event_id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    
    class Config:
        orm_mode = True


class EventWithAttendees(Event):
    attendees: List[Attendee] = [] 