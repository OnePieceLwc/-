from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RiskEvent(db.Model):
    __tablename__ = 'risk_event'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    risk_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    risk_level = db.Column(db.Float, nullable=False)
    affected_systems = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    reporter = db.relationship('User', backref=db.backref('risk_events', lazy=True))
    
    def set_affected_systems(self, systems):
        self.affected_systems = json.dumps(systems) if systems else None
    
    def get_affected_systems(self):
        return json.loads(self.affected_systems) if self.affected_systems else [] 