# 🛡️ AI Risk Intelligence Platform

Hybrid AI + Rule-Based Fraud Detection System

## 🚀 Features
- Real-time fraud detection
- Hybrid rule + AI decision engine
- Explainable AI (analyst-style reasoning)
- Risk scoring (0–100)
- Streamlit dashboard

## 🧠 Tech Stack
- FastAPI (Backend)
- Streamlit (Frontend)
- Gemini API (AI Engine)
- SQLite (Local DB)

## ⚙️ Setup

1. Clone repo
2. Create `.env` file:
   GEMINI_API_KEY=your_key_here

3. Install dependencies:
   pip install -r requirements.txt

4. Run backend:
   uvicorn backend.main:app --reload

5. Run frontend:
   streamlit run frontend/app.py
