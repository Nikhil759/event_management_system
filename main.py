from fastapi import FastAPI
from db.database import engine, Base
from api import events as events_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(events_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Management System"}
