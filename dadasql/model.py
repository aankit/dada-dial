from sqlalchemy import Column, ForeignKey, Integer, Float, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from tweetsql.database import Base

class Line(Base):
	__tablename__ = 'line'
	id = Column(Integer, primary_key=True)
	filename = Column(String(100), nullable=False)
	linenum = Column(Integer, nullable=False)
	frequency = Column(Float(precision=4), nullable=False)
	power = Column(Float(precision=4), nullable=False)


