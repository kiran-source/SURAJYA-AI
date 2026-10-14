import os
import pandas as pd
import streamlit as st
from modules.utils import converse_with_gemini_shield

def render_shield_page():
    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='margin-bottom: 4px;'>
        <h2 style='margin: 0; font-size: 1.35rem;'>
            <span style='color: #34D399; margin-right: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20" style="vertical-align: -3px; display: inline;">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="M9 12l2 2 4-4"/>
                </svg>
            </span>
            Multilingual Citizen Fraud Shield & Emergency Triage
        </h2>
        <p style='color: #64748B; font-size: 13px; margin-top: 4px;'>
            Conversational forensic assistant for real-time scam threat analysis, psychological coercion detection, and guided 1-click reporting to the National Cyber Crime Portal (1930 / cybercrime.gov.in).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ── Top Intelligence KPI Metric Bar ─────────────────────────────────────
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown("""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 10px; padding: 12px 14px;'>
            <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;'>
                <span style='font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;'>Triage Status</span>
                <span style='background: rgba(52, 211, 153, 0.15); color: #34D399; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700;'>LIVE</span>
            </div>
            <div style='font-size: 16px; font-weight: 800; color: #F1F5F9;'>24/7 Citizen Defense</div>
            <div style='font-size: 11px; color: #94A3B8; margin-top: 2px;'>National Triage Grid</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown("""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 10px; padding: 12px 14px;'>
            <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;'>
                <span style='font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;'>Language Support</span>
                <span style='background: rgba(34, 211, 238, 0.15); color: #22D3EE; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700;'>INDIC NLP</span>
            </div>
            <div style='font-size: 16px; font-weight: 800; color: #F1F5F9;'>12 Regional Dialects</div>
            <div style='font-size: 11px; color: #94A3B8; margin-top: 2px;'>Multilingual Semantic Layer</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k3:
        st.markdown("""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 10px; padding: 12px 14px;'>
            <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;'>
                <span style='font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;'>Emergency Helpline</span>
                <span style='background: rgba(251, 113, 133, 0.15); color: #FB7185; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700;'>MHA 1930</span>
            </div>
            <div style='font-size: 16px; font-weight: 800; color: #FB7185;'>National Helpline 1930</div>
            <div style='font-size: 11px; color: #94A3B8; margin-top: 2px;'>cybercrime.gov.in Integration</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k4:
        gemini_available = "GEMINI_API_KEY" in os.environ
        api_badge = ("ACTIVE", "#34D399", "rgba(52, 211, 153, 0.15)") if gemini_available else ("STANDBY", "#FBBF24", "rgba(251, 191, 36, 0.15)")
        st.markdown(f"""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 10px; padding: 12px 14px;'>
            <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;'>
                <span style='font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;'>Forensic Model</span>
                <span style='background: {api_badge[2]}; color: {api_badge[1]}; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 700;'>{api_badge[0]}</span>
            </div>
            <div style='font-size: 16px; font-weight: 800; color: #F1F5F9;'>Gemini-2.5 Flash</div>
            <div style='font-size: 11px; color: #94A3B8; margin-top: 2px;'>+ Real-time Rule Heuristics</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # ── Two-Column Layout: Incident Ingestion & Control Hub ─────────────────
    col_input_left, col_input_right = st.columns([2, 1])
    
    with col_input_right:
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px; margin-top: 0;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            Regional Language
        </h3>
        """, unsafe_allow_html=True)
        
        lang = st.selectbox(
            "Select Citizen Dialect:",
            [
                "English", 
                "हिन्दी (Hindi)", 
                "தமிழ் (Tamil)", 
                "తెలుగు (Telugu)", 
                "বাংলা (Bengali)", 
                "मराठी (Marathi)", 
                "ಕನ್ನಡ (Kannada)", 
                "മലയാളം (Malayalam)", 
                "ગુજરાતી (Gujarati)", 
                "ਪੰਜਾਬੀ (Punjabi)", 
                "ଓଡ਼ିଆ (Odia)", 
                "اردو (Urdu)"
            ],
            key="shield_lang_sel"
        )
        
        st.markdown(f"""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 8px; padding: 10px 14px; margin-bottom: 16px;'>
            <div style='font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 700;'>Active Target Dialect</div>
            <div style='font-size: 13px; font-weight: 600; color: #22D3EE; margin-top: 2px;'>{lang}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Advisory Bulletin
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.5); border: 1px solid #273449; border-radius: 8px; padding: 14px;'>
            <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="#FBBF24" stroke-width="2" width="16" height="16"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                <span style='font-size: 12px; font-weight: 700; color: #FBBF24;'>CERT-In & MHA Advisory</span>
            </div>
            <p style='font-size: 11.5px; color: #94A3B8; margin: 0 0 8px 0; line-height: 1.5;'>
                Law enforcement agencies (CBI, Customs, Police) <b>never</b> issue "Digital Arrest" warrants or freeze accounts via Skype/WhatsApp video calls.
            </p>
            <div style='display: flex; align-items: center; gap: 6px;'>
                <span style='width: 6px; height: 6px; background: #FB7185; border-radius: 50%;'></span>
                <span style='font-size: 11px; color: #FB7185; font-weight: 600;'>Immediately disconnect suspicious video calls.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_input_left:
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px; margin-top: 0;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" width="18" height="18"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            Suspicious Incident Ingestion Console
        </h3>
        """, unsafe_allow_html=True)
        
        scen = st.selectbox(
            "Quick-Start Preset Scenario (or type custom incident details below):",
            [
                "Select scenario...",
                "Received call from customs claiming package contains contraband/drugs",
                "Received text/WhatsApp proposing high returns on secret stock investment group",
                "Caller claims electricity/utility will be cutoff unless immediate transfer is done",
                "Received SMS claiming lottery or reward points won with link to login"
            ],
            key="shield_scenario_sel"
        )
        
        default_query = "" if scen == "Select scenario..." else scen
        user_query = st.text_area(
            "Describe the suspicious call, message, WhatsApp text, or link received:", 
            value=default_query, 
            height=110,
            placeholder="e.g. Someone called claiming to be CBI inspector demanding Skype video call and asking to transfer Rs 50,000 for verification...",
            key="shield_user_query"
        )
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            enable_gemini = st.checkbox(
                "🧠 Deep Gemini AI Forensic Analysis (Requires API Key)", 
                value=gemini_available, 
                key="shield_gemini_opt"
            )
        with col_btn2:
            st.markdown(f"""
            <div style='text-align: right; padding-top: 4px;'>
                <span style='font-size: 11px; color: #64748B;'>Engine: </span>
                <span style='font-size: 11px; font-weight: 600; color: {"#34D399" if gemini_available else "#FBBF24"};'>
                    {"Gemini-2.5 Flash + Rule Engine" if gemini_available else "Local Heuristic Pattern Matcher"}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
        analyze_clicked = st.button("🛡️ Analyze with SURAJYA Shield AI", use_container_width=True)

    # ── Forensic Analysis Execution & Results ────────────────────────────────
    if analyze_clicked and user_query.strip():
        gemini_active = enable_gemini and "GEMINI_API_KEY" in os.environ
        
        st.markdown("---")
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" width="20" height="20"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            Forensic Incident Triage & Safety Plan
        </h3>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns([1, 1])
        
        if gemini_active:
            with st.spinner("Executing SURAJYA Multilingual Gemini Triage Agent..."):
                res = converse_with_gemini_shield(user_query, lang)
                
            if res and "error" not in res:
                verdict = res.get("risk_level", "UNKNOWN RISK TIER").upper()
                msg = res.get("response_text", "")
                recs = res.get("action_plan", [])
                complaint_draft = res.get("ncrb_complaint_draft", "")
                
                # Determine colors and glow based on verdict
                if "RED" in verdict or "HIGH" in verdict or "CRITICAL" in verdict:
                    glow_color = "#FB7185"
                    badge_bg = "rgba(251, 113, 133, 0.15)"
                    verdict_label = "🚨 CRITICAL RISK · IMMINENT FRAUD DETECTED"
                elif "AMBER" in verdict or "YELLOW" in verdict or "MEDIUM" in verdict:
                    glow_color = "#FBBF24"
                    badge_bg = "rgba(251, 191, 36, 0.15)"
                    verdict_label = "⚠️ ELEVATED THREAT · SUSPICIOUS COERCION"
                else:
                    glow_color = "#34D399"
                    badge_bg = "rgba(52, 211, 153, 0.15)"
                    verdict_label = "🛡️ LOW RISK · STANDARD PROTOCOL"
                
                with col_res1:
                    # Inbound Citizen Dispatch Card
                    st.markdown(f"""
                    <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 18px; margin-bottom: 16px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                            <span style='font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;'>Citizen Inbound Transmission</span>
                            <span style='font-size: 11px; color: #22D3EE; background: rgba(34, 211, 238, 0.1); padding: 2px 8px; border-radius: 4px;'>{lang}</span>
                        </div>
                        <p style='color: #F1F5F9; font-size: 13.5px; font-style: italic; margin: 0; line-height: 1.5;'>
                            "{user_query}"
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Agent Verdict Dossier
                    st.markdown(f"""
                    <div style='background: #111827; border: 1px solid #1E293B; border-left: 4px solid {glow_color}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                            <div style='display: flex; align-items: center; gap: 8px;'>
                                <svg viewBox="0 0 24 24" fill="none" stroke="{glow_color}" stroke-width="2" width="20" height="20"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                                <span style='font-size: 13px; font-weight: 700; color: #F1F5F9;'>SURAJYA Forensic Response</span>
                            </div>
                            <span style='background: {badge_bg}; color: {glow_color}; font-size: 11px; font-weight: 800; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.05em;'>{verdict_label}</span>
                        </div>
                        <div style='color: #E2E8F0; font-size: 13.5px; line-height: 1.6;'>
                            {msg}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_res2:
                    # Safety Checklist
                    st.markdown("""
                    <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 18px; margin-bottom: 16px;'>
                        <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
                            <svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" width="18" height="18"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
                            <span style='font-size: 13px; font-weight: 700; color: #F1F5F9;'>Emergency Safety Action Plan</span>
                        </div>
                    """, unsafe_allow_html=True)
                    for i, r in enumerate(recs):
                        st.checkbox(f"✅ {r}", key=f"rec_ai_{i}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # NCRB Incident Draft
                    st.markdown("""
                    <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 18px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                            <div style='display: flex; align-items: center; gap: 8px;'>
                                <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                                <span style='font-size: 13px; font-weight: 700; color: #F1F5F9;'>Guided NCRB Cyber Crime Draft</span>
                            </div>
                            <a href='https://cybercrime.gov.in' target='_blank' style='font-size: 11px; color: #22D3EE; text-decoration: none; font-weight: 600;'>Open cybercrime.gov.in ↗</a>
                        </div>
                        <p style='font-size: 11.5px; color: #64748B; margin: 0 0 10px 0;'>
                            Copy this ready-to-file incident dossier directly into the official MHA National Cyber Crime Reporting Portal:
                        </p>
                    """, unsafe_allow_html=True)
                    st.code(complaint_draft, language="text")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Gemini API connection error or invalid key. Switching dynamically to local heuristic engine...")
                gemini_active = False

        if not gemini_active:
            # Fallback Local Heuristic Rule Pattern Matcher
            with col_res1:
                st.markdown(f"""
                <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 18px; margin-bottom: 16px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                        <span style='font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;'>Citizen Inbound Transmission</span>
                        <span style='font-size: 11px; color: #22D3EE; background: rgba(34, 211, 238, 0.1); padding: 2px 8px; border-radius: 4px;'>{lang}</span>
                    </div>
                    <p style='color: #F1F5F9; font-size: 13.5px; font-style: italic; margin: 0; line-height: 1.5;'>
                        "{user_query}"
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                query_lower = user_query.lower()
                if any(w in query_lower for w in ["contraband", "customs", "drugs", "arrest", "cbi", "police", "skype", "warrant"]):
                    verdict = "🚨 CRITICAL RISK · DIGITAL ARREST EXTORTION"
                    risk_color = "#FB7185"
                    risk_bg = "rgba(251, 113, 133, 0.15)"
                    risk_summary = (
                        "<b>IMPOSTER THREAT IDENTIFIED:</b> Fraud syndicates operating out of SE Asia and transnational compounds "
                        "pose as Customs officials, Narcotics Control Bureau (NCB), or CBI officers. They falsely claim contraband "
                        "was seized in your name and coerce victims into 24/7 video calls while demanding 'safe verification account transfers'. "
                        "<br/><br/><b>INDIAN LAW REALITY:</b> Police, CBI, ED, and Judicial Courts <b>never</b> execute digital arrest, "
                        "never hold judicial hearings via Skype/WhatsApp, and never demand funds to clear allegations."
                    )
                    recs = [
                        "Immediately disconnect the video call / telephone connection.",
                        "Block the scammer's phone number and reporting contact on WhatsApp / Telegram.",
                        "Never transfer funds to any 'government verification' or 'escrow' account.",
                        "Alert your local cyber cell or call National Helpline 1930 immediately.",
                        "File an official complaint with screenshots on cybercrime.gov.in."
                    ]
                elif any(w in query_lower for w in ["investment", "stock", "returns", "trading", "profit", "crypto", "vip group", "ipo"]):
                    verdict = "🚨 HIGH RISK · TASK & TRADING COMPOUND SCAM"
                    risk_color = "#FB7185"
                    risk_bg = "rgba(251, 113, 133, 0.15)"
                    risk_summary = (
                        "<b>UNAUTHORIZED INVESTMENT POOL:</b> The caller or group administrator promises guaranteed high returns, "
                        "institutional IPO allotments, or cryptocurrency arbitrage. Fraudsters use fabricated dashboard interfaces "
                        "displaying inflated profits to entice larger deposits before freezing withdrawals."
                    )
                    recs = [
                        "Do not send money to any personal or enterprise UPI/bank accounts provided in messaging groups.",
                        "Verify brokerage SEBI registration directly on the official SEBI portal (sebi.gov.in).",
                        "Exit and report the Telegram/WhatsApp channel as financial fraud.",
                        "Notify your bank immediately if any preliminary funds were transferred."
                    ]
                elif any(w in query_lower for w in ["electricity", "power", "bill", "cutoff", "disconnection", "utility"]):
                    verdict = "⚠️ ELEVATED THREAT · UTILITY COERCION PROTOCOL"
                    risk_color = "#FBBF24"
                    risk_bg = "rgba(251, 191, 36, 0.15)"
                    risk_summary = (
                        "<b>UTILITY DISCONNECTION SCARE:</b> Bulk SMS operators impersonate electricity boards (e.g. BESCOM, MSEDCL, TPDDL) "
                        "claiming power will be disconnected within hours due to unpaid dues. They instruct victims to call a fake officer "
                        "or download a malicious APK (e.g. AnyDesk, QuickSupport) to steal credentials."
                    )
                    recs = [
                        "Do not call phone numbers given in the SMS; only use official utility customer care numbers.",
                        "Never install remote screen-sharing applications (AnyDesk, TeamViewer) at caller's instruction.",
                        "Verify bill status directly on your official state electricity board website or app."
                    ]
                else:
                    verdict = "⚠️ SUSPICIOUS PROTOCOL · PHISHING & REWARD SCHEME"
                    risk_color = "#FBBF24"
                    risk_bg = "rgba(251, 191, 36, 0.15)"
                    risk_summary = (
                        "<b>UNVERIFIED INBOUND COMMUNICATION:</b> The transmission contains classic indicators of social engineering, "
                        "lure-based credential harvesting, or lottery scam targeting. Unknown senders seeking OTPs, passwords, or personal identity documents."
                    )
                    recs = [
                        "Do not click shortened links or input sensitive banking details.",
                        "Never share OTPs, PINs, or UPI credentials under any circumstances.",
                        "Verify identity through independent, verified customer service channels."
                    ]
                    
                st.markdown(f"""
                <div style='background: #111827; border: 1px solid #1E293B; border-left: 4px solid {risk_color}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                        <div style='display: flex; align-items: center; gap: 8px;'>
                            <svg viewBox="0 0 24 24" fill="none" stroke="{risk_color}" stroke-width="2" width="20" height="20"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                            <span style='font-size: 13px; font-weight: 700; color: #F1F5F9;'>SURAJYA Heuristic Verdict</span>
                        </div>
                        <span style='background: {risk_bg}; color: {risk_color}; font-size: 11px; font-weight: 800; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.05em;'>{verdict}</span>
                    </div>
                    <div style='color: #E2E8F0; font-size: 13.5px; line-height: 1.6;'>
                        {risk_summary}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_res2:
                # Local safety checklist
                st.markdown("""
                <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 18px; margin-bottom: 16px;'>
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
                        <svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" width="18" height="18"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
                        <span style='font-size: 13px; font-weight: 700; color: #F1F5F9;'>Emergency Safety Action Plan</span>
                    </div>
                """, unsafe_allow_html=True)
                for i, r in enumerate(recs):
                    st.checkbox(f"✅ {r}", key=f"rec_local_{i}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Generated Formal NCRB Complaint Dossier
                st.markdown("""
                <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 18px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                        <div style='display: flex; align-items: center; gap: 8px;'>
                            <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                            <span style='font-size: 13px; font-weight: 700; color: #F1F5F9;'>Guided NCRB Cyber Crime Incident Draft</span>
                        </div>
                        <a href='https://cybercrime.gov.in' target='_blank' style='font-size: 11px; color: #22D3EE; text-decoration: none; font-weight: 600;'>Open cybercrime.gov.in ↗</a>
                    </div>
                    <p style='font-size: 11.5px; color: #64748B; margin: 0 0 10px 0;'>
                        Copy this ready-to-file incident dossier directly into the official MHA National Cyber Crime Reporting Portal:
                    </p>
                """, unsafe_allow_html=True)
                
                complaint_draft = f"""REPORT TO: NATIONAL CYBER CRIME REPORTING PORTAL (MHA / NCRB)
================================================================================
INCIDENT CATEGORY: Online Financial Fraud / Social Engineering / Impersonation
REGISTRATION DATE: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S IST')}
SUSPECTED OFFENSE : {verdict}
COMMUNICATION LANG: {lang}

INCIDENT SUMMARY:
  - Citizen reported suspicious incoming transmission:
    "{user_query}"
  - Forensic Threat Classification: {verdict}
  - Platform/Vector: VoIP / Telephony / SMS / OTT Messaging (WhatsApp/Telegram)

EVIDENCE & MITIGATION LOG:
  - System Alert generated by SURAJYA-AI Citizen Defense Grid
  - Citizen instructed to cease communication, preserve call recordings/screenshots
  - Escalation directed to Toll-Free Cyber Crime Helpline: 1930

PORTAL SUBMISSION PORT: https://cybercrime.gov.in
================================================================================"""
                st.code(complaint_draft, language="text")
                st.markdown("</div>", unsafe_allow_html=True)
    elif not analyze_clicked:
        # Idle State: Guidance & Operational Protocol Dossier
        st.markdown("""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 12px; padding: 24px; margin-top: 10px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
                <div style='width: 32px; height: 32px; background: rgba(52, 211, 153, 0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center;'>
                    <svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                </div>
                <div>
                    <h4 style='margin: 0; font-size: 14px; font-weight: 700; color: #F1F5F9;'>How the SURAJYA Citizen Shield Operates</h4>
                    <span style='font-size: 11px; color: #64748B;'>Standard Operating Procedure for Public Scam Incident Ingestion</span>
                </div>
            </div>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 16px;'>
                <div style='background: #0C1120; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;'>
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 6px;'>
                        <span style='background: rgba(34, 211, 238, 0.15); color: #22D3EE; font-size: 11px; font-weight: 800; padding: 2px 7px; border-radius: 4px;'>STEP 01</span>
                        <span style='font-size: 12.5px; font-weight: 700; color: #F1F5F9;'>Incident Capture</span>
                    </div>
                    <p style='font-size: 11.5px; color: #94A3B8; margin: 0; line-height: 1.5;'>
                        Paste verbatim text of messages, call scripts, or WhatsApp forwards in any of 12 supported Indian regional languages.
                    </p>
                </div>
                <div style='background: #0C1120; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;'>
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 6px;'>
                        <span style='background: rgba(139, 92, 246, 0.15); color: #8B5CF6; font-size: 11px; font-weight: 800; padding: 2px 7px; border-radius: 4px;'>STEP 02</span>
                        <span style='font-size: 12.5px; font-weight: 700; color: #F1F5F9;'>Multilingual NLP Triage</span>
                    </div>
                    <p style='font-size: 11.5px; color: #94A3B8; margin: 0; line-height: 1.5;'>
                        Gemini-2.5 Flash and heuristic regex models analyze psychological coercion, fake authority lures, and credential theft vectors.
                    </p>
                </div>
                <div style='background: #0C1120; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;'>
                    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 6px;'>
                        <span style='background: rgba(52, 211, 153, 0.15); color: #34D399; font-size: 11px; font-weight: 800; padding: 2px 7px; border-radius: 4px;'>STEP 03</span>
                        <span style='font-size: 12.5px; font-weight: 700; color: #F1F5F9;'>1-Click Formal Draft</span>
                    </div>
                    <p style='font-size: 11.5px; color: #94A3B8; margin: 0; line-height: 1.5;'>
                        Receive an immediate containment checklist and a pre-formatted complaint draft for direct filing with the National Cyber Crime Reporting Portal.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
