from flask import Flask, render_template_string, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# SQLAlchemy setup
engine = create_engine('sqlite:///test.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    max_capacity = Column(Integer)
    attendees = relationship('Attendee', back_populates='event')

class Attendee(Base):
    __tablename__ = 'attendees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', back_populates='attendees')

Base.metadata.create_all(bind=engine)

# Inline HTML layout (no body placeholder)
layout = '''
<!doctype html>
<html lang="en">
<head>
<title>Event Management UI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  body {
    min-height: 100vh;
    margin: 0;
    font-family: 'Inter', Arial, sans-serif;
    background: linear-gradient(135deg, #232526 0%, #414345 100%);
    color: #f5f6fa;
    letter-spacing: 0.01em;
    position: relative;
    overflow-x: hidden;
  }
  /* Animated gradient overlay */
  body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 0;
    background: linear-gradient(270deg, #232526, #414345, #232526, #232526);
    background-size: 400% 400%;
    animation: gradientBG 18s ease infinite;
    opacity: 0.7;
  }
  @keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
  }
  /* Animated SVG waves at the bottom */
  .bg-waves {
    position: fixed;
    left: 0; right: 0; bottom: 0;
    width: 100vw;
    z-index: 1;
    pointer-events: none;
  }
  .container {
    position: relative;
    z-index: 2;
    background: rgba(34, 40, 49, 0.95);
    border-radius: 18px;
    box-shadow: 0 4px 32px #0004;
    padding: 2.5em 2em 2em 2em;
    max-width: 900px;
    margin: 2em auto;
    box-sizing: border-box;
  }
  .table-responsive {
    width: 100%;
    overflow-x: auto;
    margin-bottom: 2em;
  }
  h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5em;
    color: #fff;
    text-shadow: 0 2px 8px #0006;
  }
  nav {
    margin-bottom: 2em;
  }
  nav a {
    color: #7ed6df;
    text-decoration: none;
    font-weight: 600;
    margin-right: 1.5em;
    transition: color 0.2s;
  }
  nav a:hover {
    color: #f6e58d;
  }
  h2 {
    color: #f6e58d;
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 1em;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 2em;
    background: #232931;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px #0002;
    max-width: 100%;
    box-sizing: border-box;
  }
  th, td {
    padding: 0.65em 0.7em;
    text-align: left;
    font-size: 0.98em;
  }
  th {
    background: #393e46;
    color: #7ed6df;
    font-weight: 700;
    border-bottom: 2px solid #7ed6df33;
  }
  tr:nth-child(even) {
    background: #222831;
  }
  tr:hover {
    background: #393e46;
  }
  label {
    font-weight: 600;
    margin-bottom: 0.5em;
    display: block;
    color: #f6e58d;
  }
  input, select {
    padding: 0.5em 0.8em;
    border-radius: 6px;
    border: 1px solid #7ed6df55;
    background: #232931;
    color: #f5f6fa;
    font-size: 1em;
    margin-bottom: 1em;
    width: 100%;
    box-sizing: border-box;
    transition: border 0.2s;
  }
  input:focus, select:focus {
    border: 1.5px solid #7ed6df;
    outline: none;
  }
  button {
    background: linear-gradient(90deg, #7ed6df 0%, #70a1ff 100%);
    color: #232931;
    font-weight: 700;
    border: none;
    border-radius: 6px;
    padding: 0.7em 2em;
    font-size: 1.1em;
    cursor: pointer;
    margin-top: 0.5em;
    margin-bottom: 1.5em;
    box-shadow: 0 2px 8px #0002;
    transition: background 0.2s, color 0.2s;
  }
  button:hover {
    background: linear-gradient(90deg, #f6e58d 0%, #ffbe76 100%);
    color: #232931;
  }
  ul {
    padding-left: 1.2em;
  }
  .mb-2 { margin-bottom: 2em; }
  @media (max-width: 700px) {
    .container { padding: 1em; }
    th, td { font-size: 0.95em; padding: 0.5em 0.5em; }
    h1 { font-size: 2rem; }
    h2 { font-size: 1.2rem; }
  }
  th.start-col, th.end-col,
  td.start-col, td.end-col {
    white-space: nowrap;
    min-width: 100px;
  }
  th.location-col, td.location-col {
    max-width: 140px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
</head>
<body>
<!-- Animated SVG Waves Background -->
<svg class="bg-waves" height="220" width="100%" viewBox="0 0 1920 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="waveGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7ed6df" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#232526" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
  <path d="M0 120 Q480 220 960 120 T1920 120 V220 H0Z" fill="url(#waveGradient)">
    <animate attributeName="d" dur="8s" repeatCount="indefinite"
      values="M0 120 Q480 220 960 120 T1920 120 V220 H0Z;
              M0 100 Q480 180 960 100 T1920 100 V220 H0Z;
              M0 120 Q480 220 960 120 T1920 120 V220 H0Z" />
  </path>
</svg>
<div class="container">
<h1>Event Management System</h1>
<nav>
  <a href="/">Home</a>
  <a href="/create_event">Create Event</a>
  <a href="/db_records">View All DB Records</a>
</nav>
<hr>
{% with messages = get_flashed_messages(with_categories=True) %}
  {% if messages %}
    <ul style="list-style:none; padding-left:0;">
    {% for category, message in messages %}
      <li style="color: {% if category == 'success' %}#44bd32{% else %}#ff7979{% endif %}; font-weight:600; margin-bottom:0.5em;">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    db = SessionLocal()
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    events = db.query(Event).options(joinedload(Event.attendees)).filter(Event.start_time > now_ist).order_by(Event.start_time).all()
    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        name = request.form['name']
        email = request.form['email']
        event = db.query(Event).options(joinedload(Event.attendees)).filter(Event.id == event_id).first()
        if not event:
            flash('Event not found', 'error')
        elif db.query(Attendee).filter(Attendee.event_id == event_id, Attendee.email == email).first():
            flash('This email is already registered for this event.', 'error')
        elif len(event.attendees) >= event.max_capacity:
            flash('Event is at full capacity!', 'error')
        else:
            attendee = Attendee(name=name, email=email, event_id=event_id)
            db.add(attendee)
            db.commit()
            flash('Registration successful!', 'success')
        # Refresh events after registration
        events = db.query(Event).options(joinedload(Event.attendees)).filter(Event.start_time > now_ist).order_by(Event.start_time).all()
    db.close()
    page = '''
<h2 class="mb-2">Quick Register to an Event</h2>
<form method="post">
  <label>Event:
    <select name="event_id" required>
      <option value="">Select an event</option>
      {% for e in events %}
        <option value="{{e.id}}">{{e.name}} ({{e.location}})</option>
      {% endfor %}
    </select>
  </label><br>
  <label>Name: <input name="name" required></label><br>
  <label>Email: <input name="email" type="email" required></label><br>
  <button type="submit">Register</button>
</form>
<h2 class="mb-2">Upcoming Events</h2>
<div class="table-responsive">
<table>
<tr><th>ID</th><th>Name</th><th class="location-col">Location</th><th class="start-col">Start</th><th class="end-col">End</th><th>Capacity</th><th>Registered</th><th>Actions</th></tr>
{% for e in events %}
<tr>
  <td>{{e.id}}</td>
  <td>{{e.name}}</td>
  <td class="location-col">{{e.location}}</td>
  <td class="start-col">{{e.start_time.strftime('%Y-%m-%d %H:%M') if e.start_time else ''}}</td>
  <td class="end-col">{{e.end_time.strftime('%Y-%m-%d %H:%M') if e.end_time else ''}}</td>
  <td>{{e.max_capacity}}</td>
  <td>{{e.attendees|length}}</td>
  <td>
    <a href="/attendees/{{e.id}}">View Attendees</a>
  </td>
</tr>
{% endfor %}
</table>
</div>
'''
    return render_template_string(layout + page, events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        max_capacity = int(request.form['max_capacity'])
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except Exception:
            flash('Invalid date format. Use YYYY-MM-DDTHH:MM', 'error')
            return redirect(url_for('create_event'))
        db = SessionLocal()
        db.add(Event(name=name, location=location, start_time=start_dt, end_time=end_dt, max_capacity=max_capacity))
        db.commit()
        db.close()
        flash('Event created!', 'success')
        return redirect(url_for('home'))
    page = '''
<h2>Create Event</h2>
<form method="post">
  <label>Name: <input name="name" required></label><br>
  <label>Location: <input name="location" required></label><br>
  <label>Start Time (YYYY-MM-DDTHH:MM): <input name="start_time" required></label><br>
  <label>End Time (YYYY-MM-DDTHH:MM): <input name="end_time" required></label><br>
  <label>Max Capacity: <input name="max_capacity" type="number" min="1" required></label><br>
  <button type="submit">Create</button>
</form>
'''
    return render_template_string(layout + page)

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    db = SessionLocal()
    event = db.query(Event).options(joinedload(Event.attendees)).filter(Event.id == event_id).first()
    if not event:
        db.close()
        flash('Event not found', 'error')
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # Check for duplicates
        if db.query(Attendee).filter(Attendee.event_id == event_id, Attendee.email == email).first():
            flash('This email is already registered for this event.', 'error')
            db.close()
            return redirect(url_for('register', event_id=event_id))
        if len(event.attendees) >= event.max_capacity:
            flash('Event is at full capacity!', 'error')
            db.close()
            return redirect(url_for('register', event_id=event_id))
        attendee = Attendee(name=name, email=email, event_id=event_id)
        db.add(attendee)
        db.commit()
        db.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    db.close()
    page = '''
<h2>Register Attendee for Event: {{event.name}}</h2>
<form method="post">
  <label>Name: <input name="name" required></label><br>
  <label>Email: <input name="email" type="email" required></label><br>
  <button type="submit">Register</button>
</form>
'''
    return render_template_string(layout + page, event=event)

@app.route('/attendees/<int:event_id>')
def attendees(event_id):
    db = SessionLocal()
    event = db.query(Event).options(joinedload(Event.attendees)).filter(Event.id == event_id).first()
    attendees = event.attendees if event else []
    db.close()
    page = '''
<h2>Attendees for Event: {{ event.name if event else 'Not Found' }}</h2>
{% if attendees %}
<table>
<tr><th>ID</th><th>Name</th><th>Email</th></tr>
{% for a in attendees %}
<tr><td>{{a.id}}</td><td>{{a.name}}</td><td>{{a.email}}</td></tr>
{% endfor %}
</table>
{% else %}
<p>No attendees registered yet.</p>
{% endif %}
'''
    return render_template_string(layout + page, event=event, attendees=attendees)

@app.route('/db_records')
def db_records():
    db = SessionLocal()
    events = db.query(Event).options(joinedload(Event.attendees)).all()
    attendees = db.query(Attendee).all()
    db.close()
    page = '''
<h2>All Events</h2>
<table>
<tr><th>ID</th><th>Name</th><th>Location</th><th>Start</th><th>End</th><th>Capacity</th><th>Registered</th></tr>
{% for e in events %}
<tr><td>{{e.id}}</td><td>{{e.name}}</td><td>{{e.location}}</td><td>{{e.start_time}}</td><td>{{e.end_time}}</td><td>{{e.max_capacity}}</td><td>{{e.attendees|length}}</td></tr>
{% endfor %}
</table>
<h2>All Attendees</h2>
<table>
<tr><th>ID</th><th>Name</th><th>Email</th><th>Event ID</th></tr>
{% for a in attendees %}
<tr><td>{{a.id}}</td><td>{{a.name}}</td><td>{{a.email}}</td><td>{{a.event_id}}</td></tr>
{% endfor %}
</table>
'''
    return render_template_string(layout + page, events=events, attendees=attendees)

if __name__ == '__main__':
    app.run(debug=True) 