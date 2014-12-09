from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('mysql://root:d4d4@localhost/dada')
engine = create_engine('postgresql://tweetsql:tweetsql@127.0.0.1/dada')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import dadasql.model
    Base.metadata.create_all(bind=engine)
