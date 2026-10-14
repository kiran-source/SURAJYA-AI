# 🛡️ SURAJYA-AI: Multi-Agency Public Safety Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B.svg)](https://streamlit.io/)
[![Intelligence Grid](https://img.shields.io/badge/Status-Active%20Defense-34D399.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

> **SURAJYA-AI** is an enterprise-grade, cyber-defense intelligence suite designed for real-time digital fraud countermeasures, citizen protection, and cross-agency threat correlation. Combining machine learning heuristics, computer vision, network graph analytics, and deep Google Gemini generative forensic agents, SURAJYA-AI equips law enforcement, cyber cells, and citizens with rapid threat containment tools.

---

## 🌟 Key Platform Modules

### 1. 🏠 Platform Hub & Live Threat Telemetry
- Converged threat dashboard with persisted SQLite telemetry (`threat_registry.db`).
- Live synchronization of real-time national statistics (MHA, I4C, RBI, DoT/Sanchar Saathi).
- Multi-agency architecture monitoring: Incident Response Grid, Banking Mule Tracing, and Telecom Interception.

### 2. 📊 SIEM-Lite & Global Threat Hotspots
- Ingestion engine for web server and firewall logs (`factory_access_logs.txt`, CSV/TXT).
- Interactive Plotly analytics for threat volume, severity distribution, and temporal clustering.
- MITRE ATT&CK tactical mapping and Gemini-powered SOC Incident Playbook auto-generation.

### 3. 💵 Counterfeit Indian Currency Identification
- Dual-mode verification for ₹500, ₹200, and ₹100 notes.
- Statistical Gray-Level Co-occurrence Matrix (GLCM) texture and edge variance extraction via OpenCV.
- Manual security feature checklist audits (intaglio print, color-shifting security thread, Gandhi watermark).

### 4. 📞 Digital Arrest & Coordinated Scam Call Classifier
- Session metadata risk assessment (VoIP spoofing flags, call duration metrics).
- Ingestion of live audio recordings (WAV/MP3/M4A) with automated transcription or raw transcript text.
- Detection of psychological coercion, impersonation of CBI/Customs/Police, and MHA alert generation.

### 5. 📧 Phishing Email Forensic Analyzer
- Full email header analysis (SPF, DKIM, DMARC, origin routing relays).
- Body content scanning for credential harvesting templates, fake authority urgency, and spoofed domains.
- TF-IDF machine learning classification combined with deep Gemini forensic reasoning.

### 6. 🕸️ Transaction Graph & Money Mule Network Intelligence
- Directed multi-hop graph visualization (`networkx` & `matplotlib`).
- Dual ledger investigation: Core Banking Account Ledgers & UPI / VPA logs.
- Automated identification of money mule clustering, rapid fund layering, and cash-out destination nodes.

### 7. 💬 Multilingual Citizen Fraud Shield & Rapid Response
- Citizen-facing triage assistant supporting **12 Indic regional languages** (Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Malayalam, Gujarati, Punjabi, Odia, Urdu, English).
- Preset scenarios for Digital Arrest, fake investment groups, utility disconnection threats, and lottery scams.
- Actionable containment checklists and 1-click formatted complaint drafts for direct submission to the **National Cyber Crime Reporting Portal** ([cybercrime.gov.in](https://cybercrime.gov.in) / Toll-Free **1930**).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Optional: Google Gemini API Key (`GEMINI_API_KEY`) for generative forensic analysis

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kiran-source/SURAJYA-AI.git
   cd SURAJYA-AI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install streamlit pandas numpy scikit-learn opencv-python-headless scikit-image networkx matplotlib plotly openai
   ```

4. **(Optional) Configure Gemini API Key:**
   ```bash
   # Windows (PowerShell):
   $env:GEMINI_API_KEY="your-gemini-api-key"
   # Linux/macOS:
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

5. **Run the platform:**
   ```bash
   streamlit run app.py
   ```
   Open your browser and navigate to `http://localhost:8501`.

---

## 🏗️ Architecture

```
├── app.py                                   # Command-center shell, routing & design system
├── modules/
│   ├── landing.py                           # Platform Hub & real-time telemetry
│   ├── siem.py                              # SIEM-Lite, firewall log parsing & SOC playbooks
│   ├── currency.py                          # GLCM counterfeit currency analysis
│   ├── arrest.py                            # Digital arrest & scam call transcription
│   ├── phishing.py                          # Email header & phishing forensic scanner
│   ├── network.py                           # NetworkX money mule & transaction graphs
│   ├── shield.py                            # Multilingual citizen defense & 1930 triage
│   ├── database.py                          # SQLite threat registry & stats persistence
│   └── utils.py                             # ML model loaders & Gemini API integration
├── models/                                  # Pre-trained ML classifiers & vectorizers
├── Synthetic_Financial_datasets_small.csv   # Downsampled financial ledger dataset
├── cybersecurity_large_synthesized_data.csv # Network & SIEM intrusion telemetry
├── factory_access_logs.txt                  # Firewall sample logs
└── README.md
```

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
