import os
import random
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from modules.utils import generate_soc_playbook_with_gemini

def render_siem_page(cyber_df):
    st.markdown("""
    <div style='margin-bottom: 4px;'>
        <h2 style='margin: 0; font-size: 1.35rem;'>
            <span style='color: #3B82F6; margin-right: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20" style="vertical-align: -3px; display: inline;"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            </span>
            SIEM-Lite & Global Threat Hotspots Command Center
        </h2>
        <p style='color: #64748B; font-size: 13px; margin-top: 4px;'>Real-time telemetry, firewall log parsing, and correlation alerts tracking active digital threat vectors.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 📂 Ingest User Log File
    uploaded_logs = st.file_uploader("Ingest User Log File (CSV / TXT):", type=["csv", "txt"])
    siem_df = pd.DataFrame()
    
    if uploaded_logs is not None:
        try:
            if uploaded_logs.name.endswith(".csv"):
                siem_df = pd.read_csv(uploaded_logs)
            else:
                lines = [l.decode('utf-8').strip() for l in uploaded_logs.readlines() if l.strip()]
                parsed_list = []
                import re
                current_ip = "127.0.0.1"
                for line in lines:
                    ip_header_match = re.match(r"^(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b):$", line)
                    if ip_header_match:
                        current_ip = ip_header_match.group(1)
                        continue
                    
                    if "TIME" in line and "METHOD" in line:
                        continue
                        
                    log_match = re.match(r"^(\S+)\s+(\S+)\s+(.*?)\s+(\d{3}\s*\(.*?\)|SUCCESS|UNAUTHORIZED|\d{3})", line)
                    if log_match:
                        timestamp = log_match.group(1)
                        method = log_match.group(2)
                        request = log_match.group(3)
                        status = log_match.group(4)
                        
                        severity = "Info"
                        if "401" in status or "UNAUTHORIZED" in status:
                            severity = "Warning"
                        elif "500" in status or "ERROR" in status:
                            severity = "High"
                            
                        parsed_list.append({
                            "Timestamp": timestamp,
                            "Source IP": current_ip,
                            "Event": f"{method} {request} -> Status: {status}",
                            "Severity": severity
                        })
                    else:
                        ip_match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line)
                        severity_match = re.search(r"\b(Critical|High|Medium|Warning|Info|Low)\b", line, re.IGNORECASE)
                        
                        ip = ip_match.group(0) if ip_match else current_ip
                        severity = severity_match.group(0).capitalize() if severity_match else "Info"
                        parsed_list.append({
                            "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "Source IP": ip,
                            "Event": line,
                            "Severity": severity
                        })
                siem_df = pd.DataFrame(parsed_list)
            st.success(f"Successfully ingested and parsed {len(siem_df)} log records from {uploaded_logs.name}!")
        except Exception as ex:
            st.error(f"Error parsing log file: {ex}. Falling back to simulated log telemetry.")
            
    if siem_df.empty:
        # Generate live simulated firewall & security logs for SIEM correlation
        random.seed(101)
        ips = ["192.168.1.104", "203.111.4.15", "196.22.45.109", "10.0.0.12", "192.168.1.105"]
        events = [
            ("SSH Login Fail", "Critical"), ("Data Export 12GB", "High"), ("Port Scan detected", "High"),
            ("Normal HTTP GET", "Info"), ("Normal Database Query", "Info"), ("Normal HTTP POST", "Info"),
            ("Failed Admin Login", "Critical"), ("File upload 2MB", "Info"), ("Normal HTTP GET", "Info")
        ]
        
        # Construct a dataframe of SIEM events
        siem_logs = []
        base_time = pd.Timestamp.now() - pd.Timedelta(minutes=60)
        for i in range(50):
            time = base_time + pd.Timedelta(minutes=i * 1.2)
            ip = random.choice(ips)
            event, severity = random.choice(events)
            # Force a brute force cluster from a single IP to trigger rule
            if 15 <= i <= 18:
                ip = "196.22.45.109"
                event, severity = "SSH Login Fail", "Critical"
            # Force a large exfiltration event
            if i == 30:
                ip = "203.111.4.15"
                event, severity = "Data Export 12GB", "High"
                
            siem_logs.append({
                "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "Source IP": ip,
                "Event": event,
                "Severity": severity
            })
        siem_df = pd.DataFrame(siem_logs)
        
    if "simulated_syslog_logs" not in st.session_state:
        st.session_state["simulated_syslog_logs"] = siem_df.copy()
    siem_df = st.session_state["simulated_syslog_logs"]
    
    # ── Live Webhook Simulator ──
    st.markdown("---")
    st.markdown("""
    <h3 style='display: flex; align-items: center; gap: 8px;'>
        <svg viewBox="0 0 24 24" fill="none" stroke="#FBBF24" stroke-width="2" width="18" height="18"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        Live Threat Feed Webhook Simulator
    </h3>
    """, unsafe_allow_html=True)
    st.caption("Inject simulated live syslog payloads to stream active attack vectors directly into the SIEM correlations list.")
    
    col_sim1, col_sim2 = st.columns([3, 1])
    with col_sim1:
        sim_attack_type = st.selectbox("Select Attack Profile to Inject:", [
            "SSH Brute Force Storm (Targeting Administrative Panel)",
            "SQL Injection Probe (Targeting Core Accounts Schema)",
            "Ransomware Command & Control Ping (Targeting Financial Vault)",
            "DDoS Traffic Flooding (Targeting Public DNS Servers)",
            "Port Scan & Network Reconnaissance Heuristics"
        ])
    with col_sim2:
        st.write("")
        if st.button("Inject Webhook Payload", key="inject_webhook"):
            sim_ip = f"196.22.{random.randint(10, 250)}.{random.randint(10, 250)}"
            if "SSH" in sim_attack_type:
                e_msg = "SSH Login Fail - Admin authentication failed"
                sev = "Critical"
            elif "SQL" in sim_attack_type:
                e_msg = "SQL Injection attempt: SELECT * FROM users WHERE ID = 1' OR '1'='1"
                sev = "High"
            elif "Ransomware" in sim_attack_type:
                e_msg = "Command & Control beaconing detected to darknet node"
                sev = "Critical"
            elif "DDoS" in sim_attack_type:
                e_msg = "High rate UDP flood query stream on port 53"
                sev = "Warning"
            else:
                e_msg = "TCP Syn Port Scan detected on ports 21-8080"
                sev = "Warning"
                
            new_row = pd.DataFrame([{
                "Timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Source IP": sim_ip,
                "Event": e_msg,
                "Severity": sev
            }])
            st.session_state["simulated_syslog_logs"] = pd.concat([new_row, st.session_state["simulated_syslog_logs"]], ignore_index=True)
            st.success(f"Injected: {e_msg} (Origin: {sim_ip})")
            st.rerun()
            
    st.markdown("---")
    col_siem1, col_siem2 = st.columns([1, 1])
    
    with col_siem1:
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            SIEM-Lite Correlation Engine
        </h3>
        """, unsafe_allow_html=True)
        st.caption("Active rule correlations parsed over logs:")
        
        rule_brute = st.checkbox("Rule 1: Flag Brute Force (≥ 3 failed logins from same IP)", value=True)
        rule_exfil = st.checkbox("Rule 2: Flag Large Data Exfiltration (> 10GB external routing)", value=True)
        rule_recon = st.checkbox("Rule 3: Flag API Wildcard Reconnaissance (* queries)", value=True)
        rule_unauth = st.checkbox("Rule 4: Flag Unauthorized Access Failures (≥ 2 unauthorized requests)", value=True)
        
        # Correlate logs
        alerts = []
        if rule_brute and 'Event' in siem_df.columns:
            failed_logins = siem_df[siem_df['Event'].str.contains("Login Fail|Failed", case=False, na=False)].groupby("Source IP").size()
            for ip, count in failed_logins.items():
                if count >= 3:
                    alerts.append({
                        "Rule Match": "Brute Force Attack detected",
                        "Source IP": ip,
                        "Details": f"{count} failed logins registered within correlation window.",
                        "Severity": "Critical"
                    })
        if rule_exfil and 'Event' in siem_df.columns:
            exfil_events = siem_df[siem_df['Event'].str.contains("Data Export|Exfil|Transfer", case=False, na=False)]
            for _, row in exfil_events.iterrows():
                alerts.append({
                    "Rule Match": "Potential Data Exfiltration",
                    "Source IP": row['Source IP'],
                    "Details": f"Large outbound transfer '{row['Event']}' detected.",
                    "Severity": "High"
                })
        if rule_recon and 'Event' in siem_df.columns:
            wildcard_events = siem_df[siem_df['Event'].str.contains(r"\*", na=False)]
            reported_recon = set()
            for _, row in wildcard_events.iterrows():
                ip_route = (row['Source IP'], row['Event'])
                if ip_route not in reported_recon:
                    reported_recon.add(ip_route)
                    alerts.append({
                        "Rule Match": "Wildcard Reconnaissance Detected",
                        "Source IP": row['Source IP'],
                        "Details": f"Wildcard API query '{row['Event']}' routing request payload structures.",
                        "Severity": "High"
                    })
        if rule_unauth and 'Event' in siem_df.columns:
            unauth_events = siem_df[siem_df['Event'].str.contains("401|UNAUTHORIZED", case=False, na=False)].groupby("Source IP").size()
            for ip, count in unauth_events.items():
                if count >= 2:
                    alerts.append({
                        "Rule Match": "Persistent Unauthorized Access Attempts",
                        "Source IP": ip,
                        "Details": f"Attacker registered {count} unauthorized (401) attempts on endpoints.",
                        "Severity": "Critical"
                    })
                    
        if alerts:
            st.write("**SIEM Alerts Triggered:**")
            for alert in alerts:
                alert_color = "alert-red" if alert['Severity'] == "Critical" else "alert-orange"
                sev_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" style="vertical-align: -2px;"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
                st.markdown(f"""
                <div class='custom-alert {alert_color}'>
                    <h4>{sev_icon} {alert['Rule Match']}</h4>
                    <p><b>Attacker IP:</b> {alert['Source IP']}<br/><b>Details:</b> {alert['Details']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No SIEM rule alerts triggered. Systems nominal.")
            
    with col_siem2:
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" width="18" height="18"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            Live Event Log Stream
        </h3>
        """, unsafe_allow_html=True)
        st.dataframe(siem_df, use_container_width=True, height=260)
        
    if alerts:
        st.markdown("---")
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" width="18" height="18"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
            AI SOC Incident Responder
        </h3>
        """, unsafe_allow_html=True)
        st.caption("Review the correlation alerts using the active AI Threat Hunter:")
        if st.button("Consult AI SOC Threat Hunter"):
            with st.spinner("Analyzing alerts and generating secure containment guidelines..."):
                if "GEMINI_API_KEY" in os.environ:
                    playbook = generate_soc_playbook_with_gemini(str(alerts), str(siem_df.head(20).to_dict(orient='records')))
                else:
                    playbook = f"""# SECURITY INCIDENT RESPONSE PLAYBOOK (LOCAL FALLBACK MODE)
                    
## 1. Threat Assessment
* **Incident Alert Type**: {alerts[0]['Rule Match']}
* **Target Source IP**: {alerts[0]['Source IP']}
* **Calculated Severity**: CRITICAL
* **Details**: {alerts[0]['Details']}
* **Trigger Event Count**: {len(alerts)} active correlations.

## 2. Impact Analysis
* **Network Impact**: High risk of unauthorized traversal, credential harvesting, and shell scanning on target subnet.
* **Data Impact**: Immediate audit recommended for all transaction flows and socket endpoints related to the source IP.

## 3. Mitigation & Containment Action Plan
* **CLI Block Command (Source Attacker)**:
  `sudo iptables -A INPUT -s {alerts[0]['Source IP']} -j DROP`
* **Port Lockout Action**: Clear active sessions and drop persistent socket binds.
* **Authentication Reset**: Cycle system keys, tokens, and invalidate current active session configs.
"""
            st.code(playbook, language="markdown")
            
    st.markdown("---")
    
    if not cyber_df.empty:
        # High level stats
        c1, c2, c3, c4 = st.columns(4)
        total_incidents = len(cyber_df)
        severe_incidents = len(cyber_df[cyber_df['attack_severity'] >= 7])
        avg_response = cyber_df['response_time_min'].mean()
        compromised_data = cyber_df['data_compromised_GB'].sum()
        
        with c1:
            st.markdown(f"""
            <div class='sj-metric-card'>
                <div class='sj-metric-label'>Total Incidents</div>
                <div class='sj-metric-value' style='color: #FB7185 !important;'>{total_incidents:,}</div>
                <div class='sj-metric-source'>Simulated threat signals</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='sj-metric-card'>
                <div class='sj-metric-label'>High/Critical</div>
                <div class='sj-metric-value' style='color: #FBBF24 !important;'>{severe_incidents:,}</div>
                <div class='sj-metric-source'>Severity ≥ 7 · Requires response</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='sj-metric-card'>
                <div class='sj-metric-label'>Avg Mitigation</div>
                <div class='sj-metric-value' style='color: #22D3EE !important;'>{avg_response:.2f}<span style='font-size: 14px; color: #64748B;'> min</span></div>
                <div class='sj-metric-source'>Response-to-neutralize duration</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class='sj-metric-card'>
                <div class='sj-metric-label'>Data Compromised</div>
                <div class='sj-metric-value' style='color: #34D399 !important;'>{compromised_data:,.0f}<span style='font-size: 14px; color: #64748B;'> GB</span></div>
                <div class='sj-metric-source'>Total data breached</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Threat Map Section
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            Live Threat Activity Hotspot Map
        </h3>
        """, unsafe_allow_html=True)
        st.caption("Active cyber attack pathways connecting attacker nodes to targeted public safety systems on an interactive 3D orthographic globe.")
        
        COUNTRY_COORDS = {
            'USA': [37.0902, -95.7129],
            'Canada': [56.1304, -106.3468],
            'UK': [55.3781, -3.4360],
            'France': [46.2276, 2.2137],
            'Germany': [51.1657, 10.4515],
            'Russia': [61.5240, 105.3188],
            'China': [35.8617, 104.1954],
            'India': [20.5937, 78.9629],
            'Brazil': [-14.2350, -51.9253],
            'Australia': [-25.2744, 133.7751]
        }
        
        # Country Scope Selector
        selected_country = st.selectbox("Select Target Country Focus:", ["Global View"] + sorted(list(COUNTRY_COORDS.keys())))
        
        # Initialize simulated live counter offsets
        if "map_counter_offset" not in st.session_state:
            st.session_state["map_counter_offset"] = 0
        st.session_state["map_counter_offset"] += random.randint(1, 4)
        offset = st.session_state["map_counter_offset"]
        
        # Base stats calculations for the selected country (simulated)
        base_stats = {
            'OAS': 180000 + (offset * 12) if selected_country == "Global View" else 15000 + (offset * 3),
            'ODS': 40000 + (offset * 5) if selected_country == "Global View" else 4200 + (offset * 1),
            'MAV': 5000 + (offset * 1) if selected_country == "Global View" else 500 + random.randint(-5, 5),
            'WAV': 36000 + (offset * 8) if selected_country == "Global View" else 3500 + (offset * 2),
            'IDS': 8000 + (offset * 2) if selected_country == "Global View" else 850 + random.randint(1, 3),
            'VUL': 400 + random.randint(-2, 2) if selected_country == "Global View" else 45 + random.randint(-1, 1),
            'KAS': 40000 + (offset * 9) if selected_country == "Global View" else 4000 + (offset * 2),
            'RMW': 300 + random.randint(-1, 1) if selected_country == "Global View" else 30 + random.randint(-1, 1)
        }
        
        col_map1, col_map2 = st.columns([1.1, 2])
        
        with col_map1:
            # Kaspersky-style left panel
            disp_title = selected_country.upper() if selected_country != "Global View" else "GLOBAL REAL-TIME"
            
            stat_rows = [
                ("OAS", "On-Access Scan", base_stats['OAS'], "#34D399"),
                ("ODS", "On-Demand Scan", base_stats['ODS'], "#FB7185"),
                ("MAV", "Mail Anti-Virus", base_stats['MAV'], "#FBBF24"),
                ("WAV", "Web Anti-Virus", base_stats['WAV'], "#22D3EE"),
                ("IDS", "Intrusion Detect", base_stats['IDS'], "#8B5CF6"),
                ("VUL", "Vulnerability Scan", base_stats['VUL'], "#FBBF24"),
                ("KAS", "Anti-Spam Filter", base_stats['KAS'], "#EC4899"),
                ("RMW", "Ransomware Block", base_stats['RMW'], "#F97316"),
            ]
            
            stat_html = ""
            for abbr, label, val, color in stat_rows:
                stat_html += f"""
                    <div style='display: flex; justify-content: space-between; align-items: center; padding: 6px 0;'>
                        <span style='color: {color}; font-size: 12px; font-weight: 600;'>{abbr} <span style='color: #64748B; font-weight: 400;'>({label})</span></span>
                        <span style='font-family: "Manrope", monospace; font-weight: 700; color: #F1F5F9; font-size: 13px;'>{val:,}</span>
                    </div>
                """
            
            st.markdown(f"""
            <div class='sj-card' style='padding: 16px !important;'>
                <div style='border-bottom: 1px solid #1E293B; padding-bottom: 8px; margin-bottom: 10px;'>
                    <span style='color: #22D3EE; font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;'>Command Node</span>
                    <div style='margin-top: 4px; font-family: "Manrope", sans-serif; font-weight: 800; font-size: 14px; color: #F1F5F9;'>{disp_title}</div>
                </div>
                {stat_html}
                <div style='margin-top: 12px; border-top: 1px solid #1E293B; padding-top: 8px; text-align: center;'>
                    <span style='color: #475569; font-size: 10px;'>Telemetry feeds auto-syncing</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_map2:
            # Sample threats
            map_sample = cyber_df.sample(min(150, len(cyber_df)), random_state=42).copy()
            
            # Mapping attacker locations distinct from target locations
            countries_list = list(COUNTRY_COORDS.keys())
            attacker_locs = []
            for idx, row in map_sample.iterrows():
                loc = row['location']
                possible = [c for c in countries_list if c != loc]
                attacker_locs.append(random.choice(possible) if possible else loc)
            map_sample['attacker_location'] = attacker_locs
            
            # Apply select country filtering
            is_focused = selected_country != "Global View"
            if is_focused:
                map_sample = map_sample[(map_sample['location'] == selected_country) | (map_sample['attacker_location'] == selected_country)]
                
            import plotly.graph_objects as go
            fig_map = go.Figure()
            
            # Draw connections
            for idx, row in map_sample.iterrows():
                t_loc = row['location']
                a_loc = row['attacker_location']
                t_coord = COUNTRY_COORDS.get(t_loc, [20.5, 78.9])
                a_coord = COUNTRY_COORDS.get(a_loc, [37.0, -95.0])
                
                # Line connection
                fig_map.add_trace(go.Scattergeo(
                    lat=[a_coord[0], t_coord[0]],
                    lon=[a_coord[1], t_coord[1]],
                    mode='lines',
                    line=dict(width=1.2, color='rgba(59, 130, 246, 0.35)'),
                    hoverinfo='text',
                    text=f"Vector: {row['attack_type']} (Severity {row['attack_severity']}/10)<br/>Source: {a_loc} ({row['attacker_ip']})<br/>Target: {t_loc} ({row['target_ip']})",
                    showlegend=False
                ))
                
            # Draw Target/Attacker markers
            target_lats = [COUNTRY_COORDS.get(c, [20.5, 78.9])[0] for c in map_sample['location']]
            target_lons = [COUNTRY_COORDS.get(c, [20.5, 78.9])[1] for c in map_sample['location']]
            fig_map.add_trace(go.Scattergeo(
                lat=target_lats,
                lon=target_lons,
                mode='markers',
                marker=dict(size=7, color='#FB7185', symbol='circle', opacity=0.8),
                name='Target Nodes'
            ))
            
            attacker_lats = [COUNTRY_COORDS.get(c, [37.0, -95.0])[0] for c in map_sample['attacker_location']]
            attacker_lons = [COUNTRY_COORDS.get(c, [37.0, -95.0])[1] for c in map_sample['attacker_location']]
            fig_map.add_trace(go.Scattergeo(
                lat=attacker_lats,
                lon=attacker_lons,
                mode='markers',
                marker=dict(size=6, color='#22D3EE', symbol='triangle-up', opacity=0.7),
                name='Attacker Gateways'
            ))
            
            # Dynamic Orthographic projection zoom lock
            geo_layout = dict(
                showland=True,
                landcolor='#111827',
                showocean=True,
                oceancolor='#080B14',
                showcountries=True,
                countrycolor='#273449',
                projection_type='orthographic',
                projection_scale=1.0
            )
            
            if is_focused:
                center_c = COUNTRY_COORDS.get(selected_country, [20.5, 78.9])
                geo_layout['center'] = dict(lat=center_c[0], lon=center_c[1])
                
            fig_map.update_layout(
                geo=geo_layout,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=480,
                legend=dict(x=0.05, y=0.05, bgcolor='rgba(17, 24, 39, 0.9)', bordercolor='#273449', borderwidth=1, font=dict(color='#94A3B8', size=11))
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Display Country Telemetry details
        if is_focused:
            st.markdown("---")
            st.markdown(f"""
            <h3 style='display: flex; align-items: center; gap: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                Cyber Telemetry Focus: {selected_country}
            </h3>
            """, unsafe_allow_html=True)
            
            c_data = cyber_df[cyber_df['location'] == selected_country]
            
            if not c_data.empty:
                tc1, tc2, tc3 = st.columns(3)
                with tc1:
                    st.metric(f"Total Incidents in {selected_country}", f"{len(c_data):,}")
                with tc2:
                    st.metric("Average Severity", f"{c_data['attack_severity'].mean():.2f} / 10")
                with tc3:
                    st.metric("Total Data Leaked", f"{c_data['data_compromised_GB'].sum():,.0f} GB")
                    
                st.write("")
                col_cch1, col_cch2 = st.columns(2)
                
                with col_cch1:
                    st.write(f"**Targeted Industries in {selected_country}**")
                    ind_counts = c_data['industry'].value_counts().reset_index().head(5)
                    ind_counts.columns = ['Industry', 'Count']
                    fig_ind = px.bar(ind_counts, y='Industry', x='Count', orientation='h', color='Count', color_continuous_scale=[[0, '#1E293B'], [1, '#FB7185']])
                    fig_ind.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94A3B8', xaxis=dict(gridcolor='#1E293B'), yaxis=dict(gridcolor='#1E293B'))
                    st.plotly_chart(fig_ind, use_container_width=True)
                    
                with col_cch2:
                    st.write(f"**Mitigation Success Rate in {selected_country}**")
                    out_counts = c_data['outcome'].value_counts().reset_index()
                    out_counts.columns = ['Outcome', 'Count']
                    fig_out = px.pie(out_counts, values='Count', names='Outcome', hole=0.4, color_discrete_sequence=['#34D399', '#FB7185'])
                    fig_out.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94A3B8')
                    st.plotly_chart(fig_out, use_container_width=True)
                    
                st.write(f"**Live Target Country Incident Stream ({selected_country} Nodes):**")
                st.dataframe(
                    c_data[['timestamp', 'attacker_ip', 'attack_type', 'target_system', 'outcome', 'attack_severity']].head(10),
                    use_container_width=True
                )
            else:
                st.info(f"No local incident records parsed for {selected_country}.")
                
        # Incident Analytics Charts using Plotly
        st.markdown("---")
        st.markdown("""
        <h3 style='display: flex; align-items: center; gap: 8px;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" width="18" height="18"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            Platform Incident Analytics
        </h3>
        """, unsafe_allow_html=True)
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.write("**Event Severity Profile**")
            sev_counts = siem_df['Severity'].value_counts().reset_index()
            sev_counts.columns = ['Severity', 'Count']
            fig_pie = px.pie(sev_counts, values='Count', names='Severity', hole=0.45,
                             color_discrete_map={'Critical':'#FB7185', 'High':'#FBBF24', 'Info':'#22D3EE', 'Warning':'#F97316'})
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94A3B8')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_chart2:
            st.write("**Top Threat Actors (Attacker IPs)**")
            ip_counts = siem_df['Source IP'].value_counts().reset_index().head(10)
            ip_counts.columns = ['Source IP', 'Log Hits']
            fig_bar = px.bar(ip_counts, x='Source IP', y='Log Hits', color='Log Hits', color_continuous_scale=[[0, '#1E293B'], [0.5, '#3B82F6'], [1, '#8B5CF6']])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#94A3B8', xaxis=dict(gridcolor='#1E293B'), yaxis=dict(gridcolor='#1E293B'))
            st.plotly_chart(fig_bar, use_container_width=True)
            
    else:
        st.info("Cybersecurity threat telemetry dataset not available in workspace.")
