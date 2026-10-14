import os
import json
import pickle
import numpy as np
import pandas as pd
import cv2
import streamlit as st
from skimage.feature import graycomatrix, graycoprops

# -------------------------------------------------------------------------
# Load Pre-trained Models and Scalers (Cached)
# -------------------------------------------------------------------------
@st.cache_resource
def load_models():
    models = {}
    try:
        with open("models/currency_model.pkl", "rb") as f:
            models["currency_model"] = pickle.load(f)
        with open("models/currency_scaler.pkl", "rb") as f:
            models["currency_scaler"] = pickle.load(f)
        with open("models/scam_model.pkl", "rb") as f:
            models["scam_model"] = pickle.load(f)
        with open("models/scam_vectorizer.pkl", "rb") as f:
            models["scam_vectorizer"] = pickle.load(f)
        try:
            with open("models/phishing_model.pkl", "rb") as f:
                models["phishing_model"] = pickle.load(f)
            with open("models/phishing_vectorizer.pkl", "rb") as f:
                models["phishing_vectorizer"] = pickle.load(f)
        except Exception as ex:
            print(f"Phishing models load error: {ex}")
    except Exception as e:
        st.warning(f"Note: Local models could not be loaded. System will rely entirely on Gemini AI integration fallback. Details: {e}")
    return models

# -------------------------------------------------------------------------
# Gemini API Integration Helpers
# -------------------------------------------------------------------------
def analyze_scam_with_gemini(transcript, caller_id, risk_tier):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
        prompt = f"""
        You are an advanced digital safety forensic AI analyzing a suspicious transcript/message for law enforcement.
        Analyze the following call transcript or message:
        ---
        "{transcript}"
        ---
        Caller metadata:
        Caller ID: {caller_id}
        Assessed Risk Tier: {risk_tier}
        
        Provide your output in JSON format with the following keys:
        - "is_scam": boolean
        - "scam_probability": float (0.0 to 100.0)
        - "scam_type": string (e.g., "Digital Arrest", "Stock Investment Fraud", "Lottery Scam", "Normal Interaction")
        - "threat_vectors": list of strings (concrete indicators of fraud, e.g. "Impersonation of CBI", "Psychological coercion")
        - "detailed_reasoning": string
        - "mha_alert_narrative": string (a comprehensive detailed narrative of how the fraud compounds are trapping the citizen in this specific script)
        """
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[{'role': 'user', 'content': prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

def converse_with_gemini_shield(user_input, language):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
        prompt = f"""
        You are the SURAJYA Citizen Safety Shield chatbot.
        The user is asking you about a suspicious call, link, or message they received.
        Language requested: {language}
        
        Respond to the user's concerns directly in the requested language (or using clear trans-literated text if needed).
        Analyze if the input sounds like a scam (e.g. Digital Arrest, stock marketing VIP groups, part-time jobs, electricity bill scam).
        
        Provide your output in JSON format with the following keys:
        - "response_text": string (the chatbot response addressing the user in the selected language)
        - "risk_level": string ("GREEN", "AMBER", "RED")
        - "action_plan": list of strings (immediate step-by-step containment instructions for the user)
        - "ncrb_complaint_draft": string (a detailed draft template the user can copy and paste directly into the National Cyber Crime Reporting Portal)
        """
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[{'role': 'user', 'content': prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

def analyze_phishing_email_with_gemini(subject, body, headers):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
        prompt = f"""
        Analyze the following email for phishing indicators:
        Subject: "{subject}"
        Body: "{body}"
        Headers: "{headers}"
        
        Provide your output in JSON format with the following keys:
        - "is_phishing": boolean
        - "phishing_probability": float (0.0 to 100.0)
        - "phishing_type": string (e.g., "Credential Harvesting", "Malware Delivery", "Spear Phishing", "Safe Communication")
        - "indicators": list of strings (concrete indicators of phishing found in the text, e.g. "Mismatched sender domain", "Urgent deadline threat", "Suspicious link to unverified portal")
        - "detailed_explanation": string (clear forensic explanation of why it is or is not phishing)
        """
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[{'role': 'user', 'content': prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

def generate_soc_playbook_with_gemini(alerts, log_sample):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
        prompt = f"""
        You are an elite Lead SOC Incident Response Engineer.
        Review the following SIEM correlation alerts and log context:
        Alerts:
        {alerts}
        
        Log Sample Context:
        {log_sample}
        
        Generate a highly professional, actionable Security Incident Response Playbook detailing:
        1. Threat Assessment (identify attack type, source IP targets, and severity).
        2. Impact analysis on corporate systems.
        3. Step-by-step mitigation containment actions (e.g. CLI firewall blocks, access control updates).
        """
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating SOC playbook: {e}"

# -------------------------------------------------------------------------
# Audio Speech-to-Text Transcription Helper
# -------------------------------------------------------------------------
def convert_and_transcribe(audio_file_bytes, filename):
    import tempfile
    import librosa
    import soundfile as sf
    import speech_recognition as sr
    
    suffix = os.path.splitext(filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_in:
        temp_in.write(audio_file_bytes)
        in_path = temp_in.name
        
    out_path = in_path + ".wav"
    try:
        y, sr_rate = librosa.load(in_path, sr=16000)
        sf.write(out_path, y, sr_rate, format='WAV', subtype='PCM_16')
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(out_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        return f"Error transcribing audio: {e}"
    finally:
        for p in [in_path, out_path]:
            if os.path.exists(p):
                os.remove(p)

# Helper function to extract features for currency note validation
def extract_currency_features(image):
    if image is None:
        return None
    image_resized = cv2.resize(image, (128, 128))
    
    # 1. Color channel statistics
    img_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    r_mean, r_std = np.mean(img_rgb[:,:,0]), np.std(img_rgb[:,:,0])
    g_mean, g_std = np.mean(img_rgb[:,:,1]), np.std(img_rgb[:,:,1])
    b_mean, b_std = np.mean(img_rgb[:,:,2]), np.std(img_rgb[:,:,2])
    
    # 2. Texture features using Gray Level Co-occurrence Matrix (GLCM)
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    glcm = graycomatrix(gray, distances=[1, 3], angles=[0, np.pi/4], levels=256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast').mean()
    energy = graycoprops(glcm, 'energy').mean()
    homogeneity = graycoprops(glcm, 'homogeneity').mean()
    correlation = graycoprops(glcm, 'correlation').mean()
    
    # 3. Structural features (Edges)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges > 0)
    
    return [r_mean, r_std, g_mean, g_std, b_mean, b_std, contrast, energy, homogeneity, correlation, edge_density]

# -------------------------------------------------------------------------
# Dynamic Cybercrime Statistics Fetcher (Gemini Search & Checked Fallback)
# -------------------------------------------------------------------------
@st.cache_data(ttl=86400) # Cache statistics for 24 hours to ensure high speed
def fetch_realtime_cybercrime_stats():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {
            "active_scams": 78203,
            "scam_source": "NCRB Annual Cybercrime Report",
            "seized_notes": 222639,
            "notes_source": "RBI Annual Report (FICN Seizures)",
            "mule_accounts": 70000,
            "mule_source": "I4C MHA Bulletin (Mule Accounts Frozen)",
            "intercepted_voip": 150000,
            "voip_source": "DoT & MHA Telecom Gateway Lockouts",
            "last_updated": "2024"
        }
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
        prompt = """
        You are an elite threat intelligence analyst collecting official Indian national cybercrime stats.
        Retrieve and output the most recently verified real-world statistical figures (estimates or exact values from Ministry of Home Affairs, I4C, DoT, RBI, or NCRB) for the following parameters in India:
        1. Active/Registered Cybercrime cases or NCRP complaints (cumulative or annual).
        2. Cataloged Counterfeit Note (FICN) volumes detected or seized in Indian banking channels.
        3. Identified or frozen money mule accounts.
        4. Blocked or locked out spoofed VoIP / virtual phone connections.
        
        Provide your output in JSON format with these exact keys:
        - "active_scams": integer (e.g. annual case count, around 65000-80000)
        - "scam_source": string (citation of the official source/year, e.g. "NCRB 2023 Report")
        - "seized_notes": integer (FICN count, e.g. around 220000)
        - "notes_source": string (e.g. "RBI Annual Report 2023-24")
        - "mule_accounts": integer (frozen accounts, e.g. around 70000)
        - "mule_source": string (e.g. "MHA I4C Bulletin 2024")
        - "intercepted_voip": integer (blocked spoofed SIMs/VoIP connections, e.g. around 150000)
        - "voip_source": string (e.g. "DoT / MHA Telecom Lockouts 2024")
        - "last_updated": string (current date/year)
        """
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[{'role': 'user', 'content': prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {
            "active_scams": 78203,
            "scam_source": "NCRB Annual Cybercrime Report",
            "seized_notes": 222639,
            "notes_source": "RBI Annual Report (FICN Seizures)",
            "mule_accounts": 70000,
            "mule_source": "I4C MHA Bulletin (Mule Accounts Frozen)",
            "intercepted_voip": 150000,
            "voip_source": "DoT & MHA Telecom Gateway Lockouts",
            "last_updated": "2024"
        }
