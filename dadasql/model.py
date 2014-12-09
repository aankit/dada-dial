from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dadasql.database import Base

class Poem(Base):
	__tablename__ = 'poem'
	id = Column(Integer, primary_key=True)
	poem = Column(String(200), nullable=False)

class Line(Base):
	__tablename__ = 'line'
	id = Column(Integer, primary_key=True)
	filename = Column(String(100), nullable=False)
	fundamental_id = Column(Integer, ForeignKey('fundamental.id'), nullable=False)
	dbfs_id = Column(Integer, ForeignKey('dbfs.id'), nullable=False)
	duration_id = Column(Integer, ForeignKey('duration.id'), nullable=False)

class Fundamental(Base):
	__tablename__ = 'fundamental'
	id = Column(Integer, primary_key=True)
	frequency = Column(Integer, nullable=False)
	lines = relationship('Line', backref='fundamental')

class DBFS(Base):
	__tablename__ = 'dbfs'
	id = Column(Integer, primary_key=True)
	dbfs = Column(Integer, nullable=False)
	lines = relationship('Line', backref='dbfs')

class Duration(Base):
	__tablename__ = 'duration'
	id = Column(Integer, primary_key=True)
	duration = Column(Integer, nullable=False)
	lines = relationship('Line', backref='duration')