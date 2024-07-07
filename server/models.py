from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
import enum

db = SQLAlchemy()

class CategoryEnum(enum.Enum):
    Fiction = "Fiction"
    Non_Fiction = "Non-Fiction"

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name cannot be empty")
        # Check for uniqueness
        if Author.query.filter_by(name=name).first() is not None:
            raise ValueError("Author with this name already exists")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Author phone number must be exactly 10 digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters long")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in [category.value for category in CategoryEnum]:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'")
        return value

    @validates('title')
    def validate_title(self, key, value):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Post title must contain one of: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
