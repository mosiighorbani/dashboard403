from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime




class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    email = Column(String(128), nullable=True, unique=True)
    phone = Column(String(11), nullable=True, unique=True)
    name = Column(String(128), nullable=True)
    username = Column(String(128), nullable=True)
    password = Column(String(500), nullable=True)
    role = Column(Integer(), nullable=False, default=2)
    token = Column(String(150), nullable=True)
    code = Column(String(10), nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    login_at = Column(DateTime(), nullable=True)
    logout_at = Column(DateTime(), nullable=True)

    def __repr__(self):
        return f'{self.id} -> {self.name}'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role <= 1

    
    



