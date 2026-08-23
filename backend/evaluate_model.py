import requests
import random
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

API_URL = "http://localhost:8000/api/v1/transactions/process"

# --- 1. SYNTHETIC DATA GENERATOR ---
def generate_synthetic_data(num_samples: int = 30) -> List[Dict]:
    print(f"[INFO] Generating {num_samples} synthetic transactions for evaluation...")
    data = []
    for i in range(num_samples):
        # 30% chance of fraud injection
        is_fraud = random.random() < 0.30 
        
        if is_fraud:
            amount = random.uniform(8000.0, 50000.0)
            location = random.choice(["Lagos, Nigeria", "Moscow, Russia", "Unknown IP"])
            device = "New Unknown Device"
            ground_truth = "BLOCK"
        else:
            amount = random.uniform(10.0, 800.0)
            location = random.choice(["New York, USA", "London, UK", "San Francisco, USA"])
            device = random.choice(["iPhone 13", "MacBook Pro", "Samsung Galaxy S22"])
            ground_truth = "ALLOW"
            
        # Edge cases (Grey area - Suspicious but not guaranteed fraud)
        if random.random() < 0.10 and not is_fraud:
            amount = random.uniform(2000.0, 5000.0)
            device = "New Unknown Device"
            ground_truth = "REVIEW"
            
        tx = {
            "transaction_id": f"TEST_{i:04d}",
            "user_id": f"usr_{random.randint(100, 999)}",
            "amount": round(amount, 2),
            "location": location,
            "device": device,
            "ground_truth": ground_truth
        }
        data.append(tx)
    return data

# --- 2. API WORKER FUNCTION ---
def evaluate_transaction(tx: Dict) -> Dict:
    payload = {
        "user_id": tx["user_id"],
        "amount": tx["amount"],
        "location": tx["location"],
        "device": tx["device"]
    }
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload, timeout=15)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            # For strict binary evaluation, we treat REVIEW as BLOCK (preventative) or keep it separate.
            # Here we map AI decision to ground truth exact match.
            ai_decision = result.get("decision", "ERROR")
            
            # Binary mapping for confusion matrix (Fraud vs Not Fraud)
            # BLOCK/REVIEW = Fraud (Positive), ALLOW = Not Fraud (Negative)
            is_true_fraud = tx["ground_truth"] in ["BLOCK", "REVIEW"]
            is_pred_fraud = ai_decision in ["BLOCK", "REVIEW"]
            
            return {
                "transaction_id": tx["transaction_id"],
                "ground_truth": tx["ground_truth"],
                "ai_decision": ai_decision,
                "risk_score": result.get("risk_score"),
                "latency_sec": round(latency, 2),
                "status": "SUCCESS",
                "is_true_fraud": is_true_fraud,
                "is_pred_fraud": is_pred_fraud
            }
        else:
            return {"transaction_id": tx["transaction_id"], "status": "FAILED", "error": response.text}
    except Exception as e:
        return {"transaction_id": tx["transaction_id"], "status": "FAILED", "error": str(e)}

# --- 3. EVALUATION METRICS ENGINE ---
def calculate_metrics(results: List[Dict]):
    print("\n[INFO] Calculating Machine Learning Metrics...")
    
    successful_results = [r for r in results if r["status"] == "SUCCESS"]
    total = len(successful_results)
    
    if total == 0:
        print("[ERROR] No successful API calls. Cannot calculate metrics.")
        return
        
    true_positives = sum(1 for r in successful_results if r["is_true_fraud"] and r["is_pred_fraud"])
    true_negatives = sum(1 for r in successful_results if not r["is_true_fraud"] and not r["is_pred_fraud"])
    false_positives = sum(1 for r in successful_results if not r["is_true_fraud"] and r["is_pred_fraud"])
    false_negatives = sum(1 for r in successful_results if r["is_true_fraud"] and not r["is_pred_fraud"])
    
    accuracy = (true_positives + true_negatives) / total if total > 0 else 0
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    avg_latency = sum(r["latency_sec"] for r in successful_results) / total
    
    print("\n" + "="*50)
    print(" [REPORT] AI RISK ENGINE EVALUATION")
    print("="*50)
    print(f"Total Transactions Processed : {total}")
    print(f"Average AI Latency           : {avg_latency:.2f} seconds\n")
    
    print("--- CONFUSION MATRIX ---")
    print(f"True Positives (Fraud Caught): {true_positives}")
    print(f"True Negatives (Safe Passed) : {true_negatives}")
    print(f"False Positives (False Alarm): {false_positives}")
    print(f"False Negatives (Missed)     : {false_negatives}\n")
    
    print("--- KEY METRICS ---")
    print(f"[+] ACCURACY  : {accuracy * 100:.2f}%")
    print(f"[+] PRECISION : {precision * 100:.2f}%")
    print(f"[+] RECALL    : {recall * 100:.2f}%")
    print(f"[+] F1-SCORE  : {f1_score * 100:.2f}%")
    print("="*50)
    
    # Save report
    report = {
        "metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "avg_latency": avg_latency
        },
        "raw_results": successful_results
    }
    
    with open("evaluation_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("\n[SUCCESS] Detailed report saved to 'evaluation_report.json'")

# --- 4. MULTI-THREADED EXECUTION ---
def main():
    print("Starting AI Model Evaluation Suite...\n")
    dataset = generate_synthetic_data(num_samples=25) # 25 is safe for Gemini free tier rate limits
    results = []
    
    print(f"[INFO] Firing {len(dataset)} requests to the AI engine (Multi-threaded)...")
    
    # Use max_workers=2 to prevent hitting Gemini API rate limits too quickly
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_tx = {executor.submit(evaluate_transaction, tx): tx for tx in dataset}
        
        completed = 0
        for future in as_completed(future_to_tx):
            completed += 1
            result = future.result()
            results.append(result)
            
            if result["status"] == "SUCCESS":
                status_icon = "[PASS]" if result["is_true_fraud"] == result["is_pred_fraud"] else "[FAIL]"
                print(f"[{completed}/{len(dataset)}] {status_icon} TxID: {result['transaction_id']} | Ground Truth: {result['ground_truth']} | AI Decision: {result['ai_decision']} | Score: {result['risk_score']}")
            else:
                print(f"[{completed}/{len(dataset)}] [WARN] FAILED | Error: {result.get('error')}")
                
            # Rate limit protection for Gemini API
            time.sleep(2) 
            
    calculate_metrics(results)

if __name__ == "__main__":
    main()
