import streamlit as st
from modules.utils import fetch_realtime_cybercrime_stats

def render_landing_page():
    st.markdown("""
    <div style='margin-bottom: 4px;'>
        <h2 style='margin: 0; font-size: 1.35rem;'>
            <span style='color: #22D3EE; margin-right: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20" style="vertical-align: -3px; display: inline;">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                    <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>
            </span>
            Platform Hub & Live Threat Intelligence
        </h2>
        <p style='color: #64748B; font-size: 13px; margin-top: 4px;'>Converged threat intelligence for digital coercion interception, transaction graph analysis, and citizen fraud protection.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    from modules.database import get_dashboard_stats, update_dashboard_stat
    
    # Fetch real-time statistics directly from SQLite
    stats = get_dashboard_stats()
    
    # Sync bar
    col_sync1, col_sync2 = st.columns([3, 1])
    with col_sync1:
        st.markdown(f"""
        <div style='background: #111827; border: 1px solid #1E293B; border-radius: 8px; padding: 10px 16px; font-size: 12px; color: #64748B; display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" width="14" height="14"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span><b style='color: #94A3B8;'>NUTIR Persisted Telemetry</b> · Last Sync: <b style='color: #94A3B8;'>{stats.get('last_updated', '2024')}</b> (SQLite)</span>
        </div>
        """, unsafe_allow_html=True)
    with col_sync2:
        if st.button("⟳ Sync via Gemini", key="sync_metrics"):
            with st.spinner("Executing live search agent..."):
                new_stats = fetch_realtime_cybercrime_stats()
                for k, v in new_stats.items():
                    update_dashboard_stat(k, v)
            st.success("Successfully synchronized and persisted new metrics!")
            st.rerun()
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # ── Premium Metric Cards ──
    c1, c2, c3, c4 = st.columns(4)
    
    metrics = [
        {
            "col": c1,
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#FB7185" stroke-width="2" width="18" height="18"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            "icon_bg": "rgba(251,113,133,0.1)",
            "icon_border": "rgba(251,113,133,0.2)",
            "label": "Annual Cybercrime Cases",
            "value": f"{stats.get('active_scams', 78203):,}",
            "value_color": "#FB7185",
            "source": stats.get('scam_source', 'NCRB Report')
        },
        {
            "col": c2,
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M12 12h.01"/><path d="M17 12h.01"/><path d="M7 12h.01"/></svg>',
            "icon_bg": "rgba(34,211,238,0.1)",
            "icon_border": "rgba(34,211,238,0.2)",
            "label": "Seized Counterfeit Notes",
            "value": f"{stats.get('seized_notes', 222639):,}",
            "value_color": "#22D3EE",
            "source": stats.get('notes_source', 'RBI FICN Report')
        },
        {
            "col": c3,
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#FBBF24" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>',
            "icon_bg": "rgba(251,191,36,0.1)",
            "icon_border": "rgba(251,191,36,0.2)",
            "label": "Traced Mule A/Cs (Frozen)",
            "value": f"{stats.get('mule_accounts', 70000):,}",
            "value_color": "#FBBF24",
            "source": stats.get('mule_source', 'I4C Bulletin')
        },
        {
            "col": c4,
            "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" width="18" height="18"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
            "icon_bg": "rgba(52,211,153,0.1)",
            "icon_border": "rgba(52,211,153,0.2)",
            "label": "Blocked VoIP/SIM Lines",
            "value": f"{stats.get('intercepted_voip', 150000):,}",
            "value_color": "#34D399",
            "source": stats.get('voip_source', 'DoT/MHA Lockouts')
        }
    ]
    
    for m in metrics:
        with m["col"]:
            st.markdown(f"""
            <div class='sj-metric-card'>
                <div class='sj-metric-icon' style='background: {m["icon_bg"]}; border: 1px solid {m["icon_border"]};'>
                    {m["icon"]}
                </div>
                <div class='sj-metric-label'>{m["label"]}</div>
                <div class='sj-metric-value' style='color: {m["value_color"]} !important;'>{m["value"]}</div>
                <div class='sj-metric-source'>Source: <i>{m["source"]}</i></div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ── Landscape & Platform Impact ──
    col_state1, col_state2 = st.columns([1.2, 1])
    
    with col_state1:
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" width="18" height="18"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            Digital Fraud Landscape (2024–2026)
        </h3>
        """, unsafe_allow_html=True)
        st.markdown("""
        The Indian cybersecurity space is facing complex, highly organized, and multi-layered fraud frameworks:
        1. **Coordinated Digital Arrest Scams**: Fraud syndicates impersonate law enforcement agencies (CBI, ED, Customs, Police) over VoIP calling services, holding victims under a state of 'digital arrest' via video calls, claiming drug contraband has been sent under their credentials.
        2. **Fake Investment & VIP Trading Pools**: Coerced groups are lured into fake social messaging channels (WhatsApp, Telegram) promising SEBI-registered insider trading insights, displaying simulated gains on mock interfaces to trigger massive transfers.
        3. **Fake Indian Currency Notes (FICN)**: High-quality scanning and offset counterfeit prints continue to route through commercial retail counters, diluting economic security and requiring advanced UV and textural GLCM fiber checks.
        4. **Organized Money Mule Networks**: Stolen or purchased bank accounts (mule networks) act as routing hops to disperse stolen funds in minutes across UPI layers before converting into cryptocurrencies or cash-outs.
        """)
        
    with col_state2:
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            How SURAJYA-AI Mitigates These Vectors
        </h3>
        """, unsafe_allow_html=True)
        st.markdown("""
        * **SIEM-Lite Log Correlation**: Integrates active monitoring over corporate logs to block recon probes and unauthorized access queries before breaches compound.
        * **ML Counterfeit Currency Checks**: Deploys Computer Vision (GLCM texture audits, Canny edge microprint mapping) to provide MERCHANTS and TELLERs with immediate physical validation.
        * **Digital Arrest Voice/Script AI**: Runs VoIP calls transcriptions and parses semantic pressure markers using Gemini threat engines, generating legal Telecom block alerts automatically.
        * **UPI Transaction Trace Graphs**: Empowers INVESTIGATORs by assembling multi-hop NetworkX graphs, mapping money flow, and exporting SHA-certified Section 65B dossiers directly.
        """)

    st.markdown("---")
    
    # ── User Roles & Workspace Guides ──
    st.markdown("""
    <h3 style='display: flex; align-items: center; gap: 8px;'>
        <svg viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" width="18" height="18"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Platform User Guides & Workspace Roles
    </h3>
    """, unsafe_allow_html=True)
    st.caption("Deploy the system configurations aligned with your official role responsibilities:")
    
    rc1, rc2 = st.columns(2)
    rc3, rc4 = st.columns(2)
    
    with rc1:
        st.markdown("""
        <div class='role-card role-citizen'>
            <h3 style='color: #34D399; margin-top: 0; font-size: 1rem;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="vertical-align: -2px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                Citizens & Cyber Safe Shield
            </h3>
            <p style='color: #94A3B8 !important;'><b>Objective</b>: Verify dynamic links, check suspicious callers, and consult the regional assistant.</p>
            <ol style='padding-left: 20px; line-height: 1.7; color: #94A3B8;'>
                <li>Navigate to the <b>Citizen Fraud Shield</b> tab.</li>
                <li>Converse in English, Hindi, or regional languages to query active scams.</li>
                <li>Validate links, phone numbers, or account details.</li>
                <li>Auto-generate copyable complaint formats for the National Cyber Crime Portal.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
    with rc2:
        st.markdown("""
        <div class='role-card role-bank'>
            <h3 style='color: #22D3EE; margin-top: 0; font-size: 1rem;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="vertical-align: -2px;"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M12 12h.01"/></svg>
                Bank Tellers & Merchants
            </h3>
            <p style='color: #94A3B8 !important;'><b>Objective</b>: Scan Rs. 500 notes for microprint patterns, UV watermarks, and metallic security threads to block fake notes.</p>
            <ol style='padding-left: 20px; line-height: 1.7; color: #94A3B8;'>
                <li>Navigate to the <b>Counterfeit Currency Identification</b> tab.</li>
                <li>Load a sample test note or upload an image from your POS/Scanner.</li>
                <li>Toggle <b>UV Watermark</b> or <b>Security Thread</b> filters.</li>
                <li>Check the ML classification verdict and GLCM texture report metrics.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
    with rc3:
        st.markdown("""
        <div class='role-card role-police'>
            <h3 style='color: #8B5CF6; margin-top: 0; font-size: 1rem;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="vertical-align: -2px;"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                Investigators & Police
            </h3>
            <p style='color: #94A3B8 !important;'><b>Objective</b>: Query suspicious bank accounts, trace transaction flow hops, and identify money mule networks.</p>
            <ol style='padding-left: 20px; line-height: 1.7; color: #94A3B8;'>
                <li>Navigate to the <b>Fraud Network Graph Intelligence</b> tab.</li>
                <li>Select or input a high-risk bank account from the query dropdown.</li>
                <li>Configure trace hops and check the directed Graph AI routing map.</li>
                <li>Identify transaction values, linked destinations, and compile evidence packages.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
    with rc4:
        st.markdown("""
        <div class='role-card role-gov'>
            <h3 style='color: #FB7185; margin-top: 0; font-size: 1rem;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="vertical-align: -2px;"><path d="M3 21h18"/><path d="M3 7v1a3 3 0 0 0 6 0V7m0 1a3 3 0 0 0 6 0V7m0 1a3 3 0 0 0 6 0V7H3l2-4h14l2 4"/><path d="M5 21V10.85"/><path d="M19 21V10.85"/></svg>
                MHA & Telecom Operators
            </h3>
            <p style='color: #94A3B8 !important;'><b>Objective</b>: Analyze ongoing digital arrest scripts and voice transcriptions, triggering immediate telecom call blocks.</p>
            <ol style='padding-left: 20px; line-height: 1.7; color: #94A3B8;'>
                <li>Navigate to the <b>Digital Arrest scam detection</b> tab.</li>
                <li>Input Call Metadata (VoIP flags, caller ID, active call duration).</li>
                <li>Upload WAV/MP3 recordings for automatic Speech-to-Text transcription.</li>
                <li>Trigger the Gemini analysis scan and extract official <b>MHA Lockout Alerts</b>.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
    st.markdown("---")
    
    # ── NUTIR Registry ──
    st.markdown("""
    <h3 style='display: flex; align-items: center; gap: 8px;'>
        <svg viewBox="0 0 24 24" fill="none" stroke="#FB7185" stroke-width="2" width="18" height="18"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        National Unified Threat & Incident Registry (NUTIR)
    </h3>
    """, unsafe_allow_html=True)
    st.caption(
        "Persisted SQL Database Registry for collaborative intelligence sharing. "
        "Allows banking and law enforcement agencies to lookup suspected VPAs, domains, phone numbers, or note signatures."
    )
    
    from modules.database import get_logged_threats, search_threats
    
    # Search Box
    search_q = st.text_input("Query Suspect Registry (Search by Phone Number, IP, Domain, or Signature):", "", placeholder="e.g. +91 91234-56789 or 196.22.45.109")
    
    if search_q.strip():
        results_df = search_threats(search_q)
        if not results_df.empty:
            st.success(f"Found {len(results_df)} threat signatures matching '{search_q}':")
            st.dataframe(results_df, use_container_width=True)
        else:
            st.info(f"No records found in database matching '{search_q}'. Signatures appear clean.")
    else:
        # Show all logged threats
        threats_df = get_logged_threats()
        st.dataframe(threats_df, use_container_width=True, height=220)
