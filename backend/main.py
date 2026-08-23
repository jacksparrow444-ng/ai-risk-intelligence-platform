from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import SessionLocal, engine, Base, Transaction, get_db
from schemas import TransactionCreate, TransactionResponse
from ai_engine import evaluate_transaction_risk

app = FastAPI(title="AI Risk Manager API", version="1.0.0")

@app.post("/api/v1/transactions/process", response_model=TransactionResponse)
def process_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # 1. Simulate fetching features / Context
    transaction_dict = transaction.model_dump()
    
    # 2. Call the AI Intelligence Layer (Decisioning & Explainability)
    ai_result = evaluate_transaction_risk(transaction_dict)
    
    # 3. Log to Database
    db_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        location=transaction.location,
        device=transaction.device,
        risk_score=ai_result["risk_score"],
        decision=ai_result["decision"],
        confidence=ai_result.get("confidence", "MEDIUM"),
        next_action=ai_result.get("next_action", "Manual Review Required"),
        reasoning=ai_result["reasoning"]
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

@app.get("/api/v1/transactions", response_model=List[TransactionResponse])
def get_transactions(limit: int = 50, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).order_by(Transaction.timestamp.desc()).limit(limit).all()
    return transactions

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
