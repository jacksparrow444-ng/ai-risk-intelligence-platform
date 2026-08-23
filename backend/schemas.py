from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    location: str
    device: str

class TransactionResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    location: str
    device: str
    timestamp: datetime
    risk_score: float
    decision: str
    confidence: Optional[str] = "MEDIUM"
    next_action: Optional[str] = "Manual Review Required"
    reasoning: str

    class Config:
        from_attributes = True
