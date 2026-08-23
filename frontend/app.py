import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time
import os
import plotly.express as px

# Configure page
st.set_page_config(page_title="AI Risk Manager", page_icon="🛡️", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1/transactions")

st.title("🛡️ AI-Powered Risk Intelligence Platform")
st.info("👉 Hybrid AI + Rule-Based Risk Engine (Real-Time Decisioning)")
st.markdown("Real-time Fraud Detection & Explainability Engine MVP")

# Create tabs for the two views
tab1, tab2 = st.tabs(["🛒 Merchant Simulator (Trigger Transaction)", "📊 Risk Analyst Dashboard"])

with tab1:
    st.header("Simulate a Transaction")
    st.markdown("Use this form to trigger a transaction and see how the AI Risk Engine responds.")
    
    st.markdown("### Quick Demo Pre-fills")
    colA, colB, colC = st.columns(3)
    if colA.button("🟢 Safe Transaction"):
        st.session_state['demo_amount'] = 200.0
        st.session_state['demo_location'] = "New York, USA"
        st.session_state['demo_device'] = "MacBook Pro"
    if colB.button("🟡 Suspicious Transaction"):
        st.session_state['demo_amount'] = 8000.0
        st.session_state['demo_location'] = "New York, USA"
        st.session_state['demo_device'] = "New Unknown Device"
    if colC.button("🔴 Fraud Transaction 🚨"):
        st.session_state['demo_amount'] = 15000.0
        st.session_state['demo_location'] = "Lagos, Nigeria"
        st.session_state['demo_device'] = "New Unknown Device"
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        with col1:
            user_id = st.text_input("User ID", value="usr_12345")
            amount = st.number_input("Amount ($)", value=st.session_state.get('demo_amount', 500.0), step=10.0)
        with col2:
            location = st.text_input("Location", value=st.session_state.get('demo_location', "New York, USA"))
            
            devices = ["iPhone 13", "MacBook Pro", "New Unknown Device", "Samsung Galaxy S22"]
            default_device = st.session_state.get('demo_device', "MacBook Pro")
            index = devices.index(default_device) if default_device in devices else 0
            device = st.selectbox("Device", devices, index=index)
            
        submit_button = st.form_submit_button("Process Transaction")
        
        if submit_button:
            payload = {
                "user_id": user_id,
                "amount": amount,
                "location": location,
                "device": device
            }
            
            with st.spinner("Analyzing risk signals..."):
                start_time = time.time()
                time.sleep(1) # Fake real-time processing effect
                try:
                    response = requests.post(f"{API_URL}/process", json=payload)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Transaction Processed Successfully!")
                        
                        st.subheader("AI Decisioning Result")
                        
                        score = int(data['risk_score'])
                        if score < 30:
                            score_text = "LOW RISK"
                            st.markdown("### 🟢 Decision Summary")
                            st.markdown(f"**Decision:** 🟢 ALLOW")
                            st.markdown("**System Action:** Transaction approved and processed successfully")
                            st.success(f"**Actionable Suggestion:** {data.get('next_action', 'Proceed normally')}")
                        elif score < 70:
                            score_text = "MEDIUM RISK"
                            st.markdown("### 🟡 Decision Summary")
                            st.markdown(f"**Decision:** 🟡 REVIEW")
                            st.markdown("**System Action:** Transaction flagged for manual analyst review")
                            st.warning(f"**Actionable Suggestion:** {data.get('next_action', 'Require manual verification')}")
                        else:
                            score_text = "HIGH RISK"
                            st.markdown("### 🔴 Decision Summary")
                            st.markdown(f"**Decision:** 🔴 BLOCK")
                            st.markdown("**System Action:** Transaction blocked to prevent potential fraud")
                            st.error(f"**Actionable Suggestion:** {data.get('next_action', 'Temporarily freeze account')}")
                            
                        st.markdown("### 📈 Risk Info")
                        st.markdown(f"**Risk Score:** {score} / 100 ({score_text})")
                        st.markdown(f"**Confidence:** {data.get('confidence', 'MEDIUM')}")
                        st.markdown(f"**Fraud Probability:** {score}%")
                        
                        reasoning = data['reasoning']
                        if "**Rule-Based Risk Breakdown:**" in reasoning:
                            ai_report, rules = reasoning.split("**Rule-Based Risk Breakdown:**")
                            st.markdown("### 📊 AI Explainability Report")
                            st.markdown(ai_report.strip())
                            st.markdown("### ⚙️ Rule-Based Risk Breakdown")
                            st.markdown(rules.strip())
                        else:
                            st.markdown("### 📊 AI Explainability Report")
                            st.markdown(reasoning.strip())
                        
                        st.markdown("### ⏱ Performance")
                        st.markdown(f"Decision generated in ~{elapsed_time:.1f}s")
                        
                        # User Profiling Block
                        st.markdown("---")
                        st.markdown("### 👤 User Risk Profile (Live Update)")
                        try:
                            # Fetch user history for behavioral profiling
                            history_req = requests.get(API_URL)
                            if history_req.status_code == 200:
                                user_tx = [t for t in history_req.json() if t.get('user_id') == user_id]
                                if user_tx:
                                    total_tx = len(user_tx)
                                    avg_amt = sum(t.get('amount', 0) for t in user_tx) / total_tx
                                    max_risk = max(t.get('risk_score', 0) for t in user_tx)
                                    last_risky = next((t for t in user_tx if t.get('risk_score', 0) >= 70), None)
                                    
                                    u_col1, u_col2, u_col3 = st.columns(3)
                                    u_col1.metric("History", f"{total_tx} txs")
                                    u_col2.metric("Avg Amount", f"${avg_amt:,.2f}")
                                    u_col3.metric("Max Risk Score", f"{max_risk}/100")
                                    
                                    if last_risky:
                                        st.warning(f"**Last Risky Behavior:** {last_risky.get('decision')} on {last_risky.get('timestamp')[:10]} (Score: {last_risky.get('risk_score')})")
                                    else:
                                        st.info("**Behavioral Check:** No prior high-risk activities detected.")
                        except Exception:
                            pass
                            
                    else:
                        st.error(f"API Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}. Is FastAPI running?")

with tab2:
    st.header("Risk Analyst Dashboard")
    st.markdown("View all processed transactions and their AI-generated risk profiles.")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
        
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            transactions = response.json()
            if transactions:
                df = pd.DataFrame(transactions)
                if 'confidence' in df.columns:
                    display_df = df[['timestamp', 'user_id', 'amount', 'location', 'device', 'risk_score', 'decision', 'confidence', 'reasoning']]
                else:
                    display_df = df[['timestamp', 'user_id', 'amount', 'location', 'device', 'risk_score', 'decision', 'reasoning']]
                
                # Highlight based on decision
                def highlight_decision(val):
                    if val in ['APPROVE', 'ALLOW']: return 'color: green'
                    elif val in ['DECLINE', 'BLOCK']: return 'color: red; font-weight: bold'
                    elif val in ['CHALLENGE', 'REVIEW']: return 'color: orange'
                    return ''
                
                st.dataframe(
                    display_df.style.map(highlight_decision, subset=['decision']),
                    use_container_width=True,
                    height=300
                )
                
                # --- NEW ANALYTICS CHARTS ---
                st.markdown("---")
                st.subheader("📊 Live Analytics")
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("**📈 Last 10 Transactions Risk Trend**")
                    recent_10 = df.head(10).iloc[::-1].reset_index() # reverse to show oldest to newest left to right
                    if not recent_10.empty:
                        fig_line = px.line(recent_10, y='risk_score', markers=True, 
                                           labels={'index': 'Transaction Sequence', 'risk_score': 'Risk Score'},
                                           template="plotly_dark")
                        fig_line.add_hrect(y0=70, y1=100, line_width=0, fillcolor="red", opacity=0.2)
                        st.plotly_chart(fig_line, use_container_width=True)
                
                with chart_col2:
                    st.markdown("**🔴 High vs 🟢 Low Risk Distribution**")
                    if not df.empty:
                        fig_pie = px.pie(df, names='decision', 
                                         color='decision',
                                         color_discrete_map={'ALLOW':'green', 'APPROVE':'green', 'REVIEW':'orange', 'CHALLENGE':'orange', 'BLOCK':'red', 'DECLINE':'red'},
                                         hole=0.4,
                                         template="plotly_dark")
                        st.plotly_chart(fig_pie, use_container_width=True)
                
                # Basic metrics
                st.markdown("---")
                st.subheader("Platform Metrics")
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Total Transactions", len(df))
                m_col2.metric("Declined (Fraud)", len(df[df['decision'] == 'DECLINE']))
                m_col3.metric("Challenged (Review)", len(df[df['decision'] == 'CHALLENGE']))
                
            else:
                st.info("No transactions found yet. Use the Merchant Simulator to generate some data.")
        else:
             st.error("Failed to fetch data from API.")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}. Is FastAPI running?")
