from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import uuid

DATABASE_URL = "sqlite:///./fraud_platform.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    amount = Column(Float)
    location = Column(String)
    device = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    risk_score = Column(Float, nullable=True)
    decision = Column(String, nullable=True)
    confidence = Column(String, nullable=True)
    reasoning = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
