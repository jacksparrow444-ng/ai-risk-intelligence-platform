# 🛡️ AI-Powered Risk Intelligence Platform

👉 Hybrid AI + Rule-Based Fraud Detection System (Real-Time)

---

## 🚀 Overview

An AI-powered fraud detection platform that combines **rule-based heuristics** with **LLM-based intelligence** to make real-time transaction decisions.

It not only detects fraud but also provides **clear explainability** — just like a real fintech risk system.

---

## ⚡ Key Features

- 🧠 **Hybrid Decision Engine** (Rules + AI)
- 📊 **Real-Time Risk Scoring (0–100)**
- 🔍 **Explainable AI (Human-readable reasoning)**
- 🚫 **Fraud Detection (BLOCK / CHALLENGE / ALLOW)**
- 📱 **Device + Location Anomaly Detection**
- 📈 **Analyst-Friendly Dashboard (Streamlit UI)**
- ⏱ **Fast API Response (~3s)**

---

## 🧠 How It Works

1. **Rule Engine (Base Risk)**
   - High Amount → +20
   - New Device → +15
   - Unknown Location → +20

2. **AI Engine (LLM)**
   - Enhances risk score
   - Generates reasoning
   - Produces final decision

3. **Final Output**
   - Risk Score
   - Decision
   - Confidence
   - Explainability Report

---

## 📊 Example Output

### 🔴 BLOCK (High Risk)

- Amount: $15,000  
- New Device  
- Unknown Location  

➡️ Risk Score: **88 / 100**  
➡️ Decision: **BLOCK**

---

### 🟢 ALLOW (Low Risk)

- Normal Amount  
- Trusted Device  
- Known Location  

➡️ Risk Score: **12 / 100**  
➡️ Decision: **ALLOW**

---

## 🏗️ Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **AI Engine:** Google Gemini API
- **Database:** SQLite
- **ORM:** SQLAlchemy

---

## 📂 Project Structure
