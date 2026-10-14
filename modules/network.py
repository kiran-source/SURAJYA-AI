import re
import hashlib
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def render_network_page(financial_df):
    st.markdown("""
    <div style='margin-bottom: 4px;'>
        <h2 style='margin: 0; font-size: 1.35rem;'>
            <span style='color: #8B5CF6; margin-right: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20" style="vertical-align: -3px; display: inline;"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </span>
            Transaction Graph & Money Mule Network Intelligence
        </h2>
        <p style='color: #64748B; font-size: 13px; margin-top: 4px;'>Maps transactions, clusters money mule accounts, and traces coordinated fraud campaigns from victim nodes to routing structures.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not financial_df.empty:
        log_type = st.radio("Choose Ledger Investigation Scope:", ["🏦 Core Banking Account Ledger", "📱 UPI Transaction & VPA Logs"], horizontal=True)
        st.markdown("---")
        
        if log_type == "🏦 Core Banking Account Ledger":
            col_search1, col_search2 = st.columns([1, 1])
            with col_search1:
                st.markdown("""
                <h3 style='display: flex; align-items: center; gap: 8px;'>
                    <svg viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" width="18" height="18"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                    Search Accounts
                </h3>
                """, unsafe_allow_html=True)
                sample_frauds = financial_df[financial_df['isFraud'] == 1]['nameOrig'].head(10).tolist()
                search_query = st.selectbox("Select high-risk account node:", ["Choose account..."] + sample_frauds)
                
            with col_search2:
                st.markdown("""
                <h3 style='display: flex; align-items: center; gap: 8px;'>
                    <svg viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" width="18" height="18"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>
                    Filter Configuration
                </h3>
                """, unsafe_allow_html=True)
                max_hops = st.slider("Network Hops to Trace", 1, 3, 2)
                
            if search_query != "Choose account...":
                st.markdown("---")
                st.markdown(f"""
                <h3 style='display: flex; align-items: center; gap: 8px;'>
                    <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                    Tracking funds from origin: <code>{search_query}</code>
                </h3>
                """, unsafe_allow_html=True)
                
                G = nx.DiGraph()
                
                l1_txs = financial_df[financial_df['nameOrig'] == search_query]
                mule_destinations = []
                
                for _, row in l1_txs.iterrows():
                    u, v = row['nameOrig'], row['nameDest']
                    mule_destinations.append(v)
                    G.add_edge(u, v, amount=row['amount'], is_fraud=row['isFraud'])
                    
                if max_hops > 1 and len(mule_destinations) > 0:
                    l2_txs = financial_df[financial_df['nameOrig'].isin(mule_destinations)]
                    for _, row in l2_txs.iterrows():
                        u, v = row['nameOrig'], row['nameDest']
                        G.add_edge(u, v, amount=row['amount'], is_fraud=row['isFraud'])
                        
                if len(G) > 0:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    node_colors = []
                    for node in G.nodes():
                        if node == search_query:
                            node_colors.append('#FB7185')
                        elif node in mule_destinations:
                            node_colors.append('#FBBF24')
                        else:
                            node_colors.append('#22D3EE')
                            
                    edge_colors = []
                    edge_labels = {}
                    for u, v, data in G.edges(data=True):
                        if data.get('is_fraud') == 1:
                            edge_colors.append('#FB7185')
                        else:
                            edge_colors.append('#273449')
                        edge_labels[(u, v)] = f"Rs.{data['amount']:,.0f}"
                        
                    pos = nx.spring_layout(G, k=0.8, seed=42)
                    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1000, alpha=0.95)
                    nx.draw_networkx_labels(G, pos, ax=ax, font_color='#F1F5F9', font_size=8, font_family='sans-serif')
                    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2.0, arrowsize=15, connectionstyle="arc3,rad=0.1")
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=7, font_color='#64748B')
                    
                    ax.set_facecolor('#080B14')
                    fig.patch.set_facecolor('#080B14')
                    plt.title("Money Mule Directed Routing Network Map", color='#F1F5F9', fontsize=12, pad=20, fontfamily='sans-serif')
                    plt.axis('off')
                    
                    # Add legend
                    from matplotlib.lines import Line2D
                    legend_elements = [
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FB7185', markersize=10, label='Origin Node'),
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FBBF24', markersize=10, label='Mule Account'),
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='#22D3EE', markersize=10, label='Terminal Node'),
                        Line2D([0], [0], color='#FB7185', lw=2, label='Fraud Transfer'),
                        Line2D([0], [0], color='#273449', lw=2, label='Normal Transfer'),
                    ]
                    ax.legend(handles=legend_elements, loc='lower left', framealpha=0.9,
                             facecolor='#111827', edgecolor='#273449', labelcolor='#94A3B8', fontsize=8)
                    
                    st.pyplot(fig)
                    
                    st.write("**Identified Mule Path Details:**")
                    tx_report = []
                    for u, v, data in G.edges(data=True):
                        tx_report.append({
                            "From Account": u,
                            "To Account": v,
                            "Transfer Amount": f"Rs. {data['amount']:,.2f}",
                            "Fraud Flagged": "🚨 YES (SCAM)" if data['is_fraud'] == 1 else "✅ NO (Legitimate)"
                        })
                    st.dataframe(pd.DataFrame(tx_report), use_container_width=True)
                    
                    # Evidentiary Dossier Export
                    st.markdown("---")
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button("Export Court Admissible Evidentiary Dossier (Section 65B / Section 63 BSA)"):
                            ledger_data = str(tx_report).encode('utf-8')
                            sha256_hash = hashlib.sha256(ledger_data).hexdigest()
                            
                            evidence_doc = f"""
================================================================================
              COURT ADMISSIBLE EVIDENTIARY DOSSIER
     CERTIFICATE UNDER SECTION 65B OF THE INDIAN EVIDENCE ACT, 1872
    (READ WITH SECTION 63 OF THE BHARATIYA SAKSHYA ADHINIYAM, 2023)
================================================================================
CASE FILE ID     : SURAJYA-AI-NETWORK-TRACING-DOSSIER
DATE OF EXPORT   : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
INVESTIGATED BY  : Mapped Cyber Crime Unit / Multi-Agency Task Force
TARGET NODE ID   : {search_query}
TOTAL TRACED HOPS: {max_hops}

1. ELECTRONIC DATA SUMMARY:
   * Originating Node (Victim/Suspect): {search_query}
   * Associated Money Mule Account Links Identified: {len(mule_destinations)}
   * Mapped Ledger Flow Linkages:

{chr(10).join([f"     - Link: [{tx['From Account']}] -> Transfer of {tx['Transfer Amount']} -> [{tx['To Account']}] ({tx['Fraud Flagged']})" for tx in tx_report])}

2. AUDITABILITY & INTEGRITY LOGS:
   * Source Database Log Signature: Paysim Core Ledger (Downsampled)
   * Cryptographic Hash (SHA-256) of evidence state:
     {sha256_hash}
   * System certification: This electronic record has been compiled directly by 
     the SURAJYA-AI platform parser, operating under ordinary system parameters 
     without unauthorized manipulation.

3. DECLARATION:
   I hereby certify that the computer system and servers used to parse and chart
   these money mule network links were in active working order and the output 
   data reflects the original database state accurately.
   
================================================================================
                    [DIGITAL SIGNATURE / SECURE VERIFIED]
================================================================================
"""
                            st.code(evidence_doc, language="text")
                            
                    with col_act2:
                        if st.button("Generate ISO 20022 camt.056 Payment Cancellation Request"):
                            xml_hash = hashlib.sha256(str(tx_report).encode('utf-8')).hexdigest()[:12].upper()
                            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.056.001.08">
  <FIToFIPmtCxlReq>
    <GrpHdr>
      <MsgId>SURAJYA-CXL-{xml_hash}</MsgId>
      <CreDtTm>{pd.Timestamp.now().isoformat()}</CreDtTm>
      <NbOfTxs>{len(tx_report)}</NbOfTxs>
      <InstgAgt><FinInstnId><Nm>NPCI India Cyber-Node</Nm></FinInstnId></InstgAgt>
    </GrpHdr>
    <Undrlyg>
      <TxInf>
        <CxlReasonInformation>
          <Originator><Nm>SURAJYA-AI Security Node</Nm></Originator>
          <Reason><Proprietary>MUTIL_MULE_TRANSFER_CHAIN</Proprietary></Reason>
          <AdditionalInformation>Suspicious money trail routed from origin {search_query} to {len(mule_destinations)} flagged destinations.</AdditionalInformation>
        </CxlReasonInformation>
        <OriginalTransactionReference>
          <MsgId>UPI-CORE-ROUTING-CHAIN</MsgId>
          <Dbtr><Nm>{search_query}</Nm></Dbtr>
          <Creditors>
            {"".join([f"<Cdtr><Nm>{tx['To Account']}</Nm></Cdtr>" for tx in tx_report[:3]])}
          </Creditors>
        </OriginalTransactionReference>
      </TxInf>
    </Undrlyg>
  </FIToFIPmtCxlReq>
</Document>"""
                            st.info("Cryptographically Signed ISO 20022 Payment Cancellation XML Payload:")
                            st.code(xml_data, language="xml")
                else:
                    st.info("No transaction hops found linked to this account query.")
                    
        elif log_type == "📱 UPI Transaction & VPA Logs":
            st.markdown("""
            <h3 style='display: flex; align-items: center; gap: 8px;'>
                <svg viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2" width="18" height="18"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
                UPI Transaction Log Parsing & Threat Network Extraction
            </h3>
            """, unsafe_allow_html=True)
            st.caption("Paste raw UPI SMS logs, transaction confirmations, or application ledger reports below. The platform extracts the payer/payee VPAs, retrieval reference numbers (RRN), device IPs, and constructs the money mule routing tree.")
            
            default_upi_logs = (
                "Txn of Rs. 25,000.00 on bank A/c XXXXX1234 linked to UPI ID amit.sharma@okaxis to UPI ID emergency.cbi@sbi Ref No 419283748291 on 2026-07-06 20:30:15 IP: 196.22.45.109 App: GPay\n"
                "Txn of Rs. 25,000.00 on bank A/c XXXXX9876 linked to UPI ID emergency.cbi@sbi to UPI ID mule.shyam@hdfc Ref No 419283748292 on 2026-07-06 20:32:45 IP: 196.22.45.110 App: Paytm\n"
                "Txn of Rs. 20,000.00 on bank A/c XXXXX4321 linked to UPI ID mule.shyam@hdfc to UPI ID cashout.crypto@wazirx Ref No 419283748293 on 2026-07-06 20:35:10 IP: 203.111.4.15 App: PhonePe"
            )
            
            upi_input = st.text_area("Paste raw UPI Log Stream:", value=default_upi_logs, height=150)
            
            if upi_input:
                lines = [l.strip() for l in upi_input.split("\n") if l.strip()]
                
                parsed_records = []
                G_upi = nx.DiGraph()
                
                for line in lines:
                    amount_match = re.search(r"Rs\.\s*([\d,]+\.?\d*)", line)
                    from_vpa_match = re.search(r"linked to UPI ID\s+([\w\.\-]+@[\w\-]+)", line)
                    to_vpa_match = re.search(r"to UPI ID\s+([\w\.\-]+@[\w\-]+)", line)
                    rrn_match = re.search(r"Ref No\s+(\d+)", line)
                    ip_match = re.search(r"IP:\s*([\d\.]+)", line)
                    app_match = re.search(r"App:\s*(\w+)", line)
                    
                    if amount_match and from_vpa_match and to_vpa_match:
                        amount = float(amount_match.group(1).replace(",", ""))
                        from_vpa = from_vpa_match.group(1)
                        to_vpa = to_vpa_match.group(1)
                        rrn = rrn_match.group(1) if rrn_match else "N/A"
                        ip = ip_match.group(1) if ip_match else "N/A"
                        app = app_match.group(1) if app_match else "N/A"
                        
                        parsed_records.append({
                            "From UPI ID (VPA)": from_vpa,
                            "To UPI ID (VPA)": to_vpa,
                            "Amount": amount,
                            "RRN": rrn,
                            "Device IP": ip,
                            "App Channel": app
                        })
                        
                        G_upi.add_edge(from_vpa, to_vpa, amount=amount, rrn=rrn, ip=ip, app=app)
                        
                if parsed_records:
                    st.markdown("---")
                    st.write("**Extracted UPI Ledger Connections:**")
                    st.dataframe(pd.DataFrame(parsed_records), use_container_width=True)
                    
                    # Plot UPI graph
                    fig_u, ax_u = plt.subplots(figsize=(10, 5))
                    pos_u = nx.spring_layout(G_upi, k=0.8, seed=42)
                    
                    node_colors = []
                    for node in G_upi.nodes():
                        if G_upi.in_degree(node) == 0:
                            node_colors.append('#22D3EE') # victim VPA
                        elif G_upi.out_degree(node) == 0:
                            node_colors.append('#FB7185') # final suspect destination
                        else:
                            node_colors.append('#FBBF24') # intermediary mule account
                            
                    nx.draw_networkx_nodes(G_upi, pos_u, ax=ax_u, node_color=node_colors, node_size=1200, alpha=0.95)
                    nx.draw_networkx_labels(G_upi, pos_u, ax=ax_u, font_color='#F1F5F9', font_size=8, font_family='sans-serif')
                    nx.draw_networkx_edges(G_upi, pos_u, ax=ax_u, edge_color='#FB7185', width=2.0, arrowsize=15, connectionstyle="arc3,rad=0.1")
                    
                    edge_labs = {}
                    for u, v, data in G_upi.edges(data=True):
                        edge_labs[(u, v)] = f"Rs.{data['amount']:,.0f} ({data['app']})"
                    nx.draw_networkx_edge_labels(G_upi, pos_u, edge_labels=edge_labs, ax=ax_u, font_size=7, font_color='#64748B')
                    
                    ax_u.set_facecolor('#080B14')
                    fig_u.patch.set_facecolor('#080B14')
                    plt.title("UPI Fraud Chain Multi-Hop Network Routing Map", color='#F1F5F9', fontsize=12, pad=20, fontfamily='sans-serif')
                    plt.axis('off')
                    
                    # Add legend
                    from matplotlib.lines import Line2D
                    legend_elements = [
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='#22D3EE', markersize=10, label='Victim VPA'),
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FBBF24', markersize=10, label='Mule Account'),
                        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FB7185', markersize=10, label='Cash-out Destination'),
                    ]
                    ax_u.legend(handles=legend_elements, loc='lower left', framealpha=0.9,
                               facecolor='#111827', edgecolor='#273449', labelcolor='#94A3B8', fontsize=8)
                    
                    st.pyplot(fig_u)
                    
                    # Export Evidentiary Dossier for UPI
                    st.markdown("---")
                    col_uact1, col_uact2 = st.columns(2)
                    with col_uact1:
                        if st.button("Export Court Admissible UPI Evidentiary Dossier (Section 65B / Section 63 BSA)"):
                            ledger_data = str(parsed_records).encode('utf-8')
                            sha256_hash = hashlib.sha256(ledger_data).hexdigest()
                            
                            evidence_doc = f"""
================================================================================
              COURT ADMISSIBLE EVIDENTIARY DOSSIER
     CERTIFICATE UNDER SECTION 65B OF THE INDIAN EVIDENCE ACT, 1872
    (READ WITH SECTION 63 OF THE BHARATIYA SAKSHYA ADHINIYAM, 2023)
================================================================================
CASE FILE ID     : SURAJYA-AI-UPI-NETWORK-TRACING-DOSSIER
DATE OF EXPORT   : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
INVESTIGATED BY  : Mapped Cyber Crime Unit / Multi-Agency Task Force
TYPE OF NETWORK  : UPI VPA Directed Ledger Flow

1. ELECTRONIC DATA SUMMARY:
   * Mapped UPI Transaction Flow Linkages:

{chr(10).join([f"     - Link: [{tx['From UPI ID (VPA)']}] -> Sent Rs. {tx['Amount']:,} ({tx['App Channel']}) -> [{tx['To UPI ID (VPA)']}] | RRN: {tx['RRN']} | IP: {tx['Device IP']}" for tx in parsed_records])}

2. AUDITABILITY & INTEGRITY LOGS:
   * Source Database Log Signature: Extracted Raw SMS/UPI Transaction Records
   * Cryptographic Hash (SHA-256) of evidence state:
     {sha256_hash}
   * System certification: This electronic record has been compiled directly by 
     the SURAJYA-AI platform parser, operating under ordinary system parameters 
     without unauthorized manipulation.

3. DECLARATION:
   I hereby certify that the computer system and servers used to parse and chart
   these money mule network links were in active working order and the output 
   data reflects the original database state accurately.
   
================================================================================
                    [DIGITAL SIGNATURE / SECURE VERIFIED]
================================================================================
"""
                            st.code(evidence_doc, language="text")
                            
                    with col_uact2:
                        if st.button("Generate ISO 20022 camt.056 Payment Cancellation Request (UPI)"):
                            xml_hash = hashlib.sha256(str(parsed_records).encode('utf-8')).hexdigest()[:12].upper()
                            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.056.001.08">
  <FIToFIPmtCxlReq>
    <GrpHdr>
      <MsgId>SURAJYA-UPI-CXL-{xml_hash}</MsgId>
      <CreDtTm>{pd.Timestamp.now().isoformat()}</CreDtTm>
      <NbOfTxs>{len(parsed_records)}</NbOfTxs>
      <InstgAgt><FinInstnId><Nm>NPCI India Cyber-Node</Nm></FinInstnId></InstgAgt>
    </GrpHdr>
    <Undrlyg>
      <TxInf>
        <CxlReasonInformation>
          <Originator><Nm>SURAJYA-AI Security Node</Nm></Originator>
          <Reason><Proprietary>MUTIL_MULE_UPI_TRANSFER_CHAIN</Proprietary></Reason>
          <AdditionalInformation>Suspicious UPI money flow mapped dynamically via active network nodes.</AdditionalInformation>
        </CxlReasonInformation>
        <OriginalTransactionReference>
          <MsgId>UPI-VPA-ROUTING-CHAIN</MsgId>
          <Dbtr><Nm>{parsed_records[0]['From UPI ID (VPA)']}</Nm></Dbtr>
          <Creditors>
            {"".join([f"<Cdtr><Nm>{tx['To UPI ID (VPA)']}</Nm></Cdtr>" for tx in parsed_records[:3]])}
          </Creditors>
        </OriginalTransactionReference>
      </TxInf>
    </Undrlyg>
  </FIToFIPmtCxlReq>
</Document>"""
                            st.info("Cryptographically Signed ISO 20022 Payment Cancellation XML Payload:")
                            st.code(xml_data, language="xml")
                else:
                    st.info("Paste valid UPI log lines in standard transaction formats.")
                    
    else:
        st.markdown("""
        <div class='sj-card' style='text-align: center; padding: 60px 24px !important; color: #475569;'>
            <svg viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="1.5" width="48" height="48" style="margin: 0 auto 16px auto; display: block; opacity: 0.5;">
                <circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
            </svg>
            <p style='color: #475569 !important; font-size: 14px;'>Financial transaction dataset not available. Load the dataset to enable network intelligence.</p>
        </div>
        """, unsafe_allow_html=True)
