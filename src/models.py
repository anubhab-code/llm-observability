from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    prompt = Column(String)
    response = Column(String)
    latency_ms = Column(Float)
    total_tokens = Column(Integer)
    cost_usd = Column(Float)
    model = Column(String)
    provider = Column(String)
    status = Column(String)
    feedback = Column(String)
    category = Column(String)
    hallucination = Column(Boolean)
    similarity_score = Column(Float)

engine = create_engine("sqlite:///observability.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)