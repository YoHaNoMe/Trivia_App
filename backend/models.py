import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_name = "trivia"
database_path = "postgres:///{}".format(database_name)

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()

'''
Question

'''
class Question(db.Model):
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category_id, difficulty):
    self.question = question
    self.answer = answer
    self.category_id = category_id
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': Category.query.get(self.category_id).type,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)
  questions = db.relationship('Question', backref='category', lazy=True)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }
