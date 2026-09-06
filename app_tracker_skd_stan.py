import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# Page Configuration
st.set_page_config(
    page_title="Tracker SKD PKN STAN 2026",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File Storage Path
DATA_FILE = "skd_stan_tryout_data.csv"

# Function to load data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Tanggal", "Nama_TO", "TWK_Benar", "TWK_Salah", "TWK_Skor",
            "TIU_Benar", "TIU_Salah", "TIU_Skor",
            "TKP_P5", "TKP_P4", "TKP_P3", "TKP_P2", "TKP_P1", "TKP_P0", "TKP_Skor",
            "Total_Skor", "Total_Benar", "Total_Salah", "Status"
        ])

# Function to save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Load existing data into session state
if "df_to" not in st.session_state:
    st.session_state.df_to = load_data()

# Function to evaluate status based on targets
def scan_status(total_score, twk_score, tiu_score, tkp_score, twk_benar, tiu_benar, tkp_p5):
    # Target Criteria PKN STAN 2026:
    # Target Total >= 470
    # TWK >= 115 (Benar >= 23)
    # TIU >= 150 (Benar >= 30)
    # TKP >= 175 (P5 >= 35)
    
    twk_pass = (twk_score >= 115) and (twk_benar >= 23)
    tiu_pass = (tiu_score >= 150) and (tiu_benar >= 30)
    tkp_pass = (tkp_score >= 175) and (tkp_p5 >= 35)
    
    # Check for Exceeding Target (Melampaui Target)
    if total_score >= 490 and twk_score >= 125 and tiu_score >= 160 and tkp_score >= 185:
        return "Melampaui Target", "🟢🟢", "#10B981"  # Emerald
    # Check for Meeting Target (Sudah Mencapai Target)
    elif total_score >= 470 and twk_pass and tiu_pass and tkp_pass:
        return "Sudah Mencapai Target", "🟢", "#059669"  # Green
    # Check for Almost Meeting Target (Hampir Mencapai Target)
    elif total_score >= 430 or (sum([twk_pass, tiu_pass, tkp_pass]) >= 2):
        return "Hampir Mencapai Target", "🟡", "#D97706"  # Amber
    else:
        return "Belum Mencapai Target", "🔴", "#DC2626"  # Red

# App Header
st.title("🎯 Pemantau Statistik Kesiapan SKD PKN STAN 2026")
st.caption("Aplikasi Analisis & Diagnostik Tryout Kedinasan Mandiri")

# Sidebar - Target Reference & Instructions
with st.sidebar:
    st.header("🎯 Target Paten PKN STAN 2026")
    st.markdown("""
    ---
    **Target Total SKD:** **470+** / 550
    
    * **TWK (30 Soal):**
      - Min Skor: **115 - 125**
      - Min Benar: **23 - 25 Soal**
    * **TIU (35 Soal):**
      - Min Skor: **150 - 160**
      - Min Benar: **30 - 32 Soal**
    * **TKP (45 Soal):**
      - Min Skor: **175+**
      - Min Poin 5: **35 - 40 Soal**
      - Min Poin 4: **35 Soal**
    ---
    """)
    st.info("💡 Input hasil Tryout kamu di tab 'Input Tryout', lalu pantau progres di grafik & tabel ringkasan.")

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["📝 Input Data Tryout", "📊 Dashboard & Analytics", "📜 Riwayat & Kelola Data"])

# ==================== TAB 1: INPUT DATA ====================
with tab1:
    st.subheader("Input Hasil Tryout Baru")
    
    with st.form("form_tryout", clear_on_submit=True):
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            nama_to = st.text_input("Nama / Sesi Tryout", placeholder="Contoh: Tryout Akbar #1 - Brain Academy")
        with col_meta2:
            tanggal = st.date_input("Tanggal Pelaksanaan")
            
        st.markdown("---")
        st.markdown("### 1. Tes Wawasan Kebangsaan (TWK) - 30 Soal")
        col_twk1, col_twk2 = st.columns(2)
        with col_twk1:
            twk_benar = st.number_input("TWK Jumlah Benar", min_value=0, max_value=30, value=20)
        with col_twk2:
            twk_salah = st.number_input("TWK Jumlah Salah / Kosong", min_value=0, max_value=30, value=10)
            
        st.markdown("---")
        st.markdown("### 2. Tes Inteligensia Umum (TIU) - 35 Soal")
        col_tiu1, col_tiu2 = st.columns(2)
        with col_tiu1:
            tiu_benar = st.number_input("TIU Jumlah Benar", min_value=0, max_value=35, value=25)
        with col_tiu2:
            tiu_salah = st.number_input("TIU Jumlah Salah / Kosong", min_value=0, max_value=35, value=10)
            
        st.markdown("---")
        st.markdown("### 3. Tes Karakteristik Pribadi (TKP) - 45 Soal (Rincian Poin 1 - 5)")
        
        col_tkp1, col_tkp2, col_tkp3 = st.columns(3)
        with col_tkp1:
            tkp_p5 = st.number_input("Jumlah Soal Poin 5", min_value=0, max_value=45, value=30)
            tkp_p4 = st.number_input("Jumlah Soal Poin 4", min_value=0, max_value=45, value=10)
        with col_tkp2:
            tkp_p3 = st.number_input("Jumlah Soal Poin 3", min_value=0, max_value=45, value=5)
            tkp_p2 = st.number_input("Jumlah Soal Poin 2", min_value=0, max_value=45, value=0)
        with col_tkp3:
            tkp_p1 = st.number_input("Jumlah Soal Poin 1", min_value=0, max_value=45, value=0)
            tkp_p0 = st.number_input("Jumlah Soal Tidak Dijawab (Poin 0)", min_value=0, max_value=45, value=0)

        total_tkp_soal = tkp_p5 + tkp_p4 + tkp_p3 + tkp_p2 + tkp_p1 + tkp_p0
        if total_tkp_soal != 45:
            st.warning(f"⚠️ Total soal TKP yang dimasukkan: **{total_tkp_soal}/45**. Pastikan totalnya pas 45 soal.")
            
        submitted = st.form_submit_button("💾 Simpan Data Tryout", use_container_width=True)
        
        if submitted:
            if not nama_to:
                st.error("Mohon isi Nama/Sesi Tryout terlebih dahulu.")
            else:
                # Calculations
                twk_skor = twk_benar * 5
                tiu_skor = tiu_benar * 5
                tkp_skor = (tkp_p5 * 5) + (tkp_p4 * 4) + (tkp_p3 * 3) + (tkp_p2 * 2) + (tkp_p1 * 1)
                
                total_skor = twk_skor + tiu_skor + tkp_skor
                total_benar = twk_benar + tiu_benar + (tkp_p5 + tkp_p4) # P5 & P4 dianggap jawaban berkategori tinggi
                total_salah = twk_salah + tiu_salah + (tkp_p3 + tkp_p2 + tkp_p1 + tkp_p0)
                
                status_text, icon, color = scan_status(
                    total_skor, twk_skor, tiu_skor, tkp_skor, twk_benar, tiu_benar, tkp_p5
                )
                
                new_row = {
                    "Tanggal": str(tanggal),
                    "Nama_TO": nama_to,
                    "TWK_Benar": twk_benar,
                    "TWK_Salah": twk_salah,
                    "TWK_Skor": twk_skor,
                    "TIU_Benar": tiu_benar,
                    "TIU_Salah": tiu_salah,
                    "TIU_Skor": tiu_skor,
                    "TKP_P5": tkp_p5,
                    "TKP_P4": tkp_p4,
                    "TKP_P3": tkp_p3,
                    "TKP_P2": tkp_p2,
                    "TKP_P1": tkp_p1,
                    "TKP_P0": tkp_p0,
                    "TKP_Skor": tkp_skor,
                    "Total_Skor": total_skor,
                    "Total_Benar": total_benar,
                    "Total_Salah": total_salah,
                    "Status": status_text
                }
                
                st.session_state.df_to = pd.concat([st.session_state.df_to, pd.DataFrame([new_row])], ignore_index=True)
                save_data(st.session_state.df_to)
                st.success(f"✅ Data '{nama_to}' berhasil disimpan!")
                st.rerun()

# ==================== TAB 2: DASHBOARD & ANALYTICS ====================
with tab2:
    if st.session_state.df_to.empty:
        st.info("Belum ada data Tryout. Silakan masukan data pada tab 'Input Data Tryout'.")
    else:
        df = st.session_state.df_to.copy()
        latest = df.iloc[-1]
        
        # Header Status Pemindai Otomatis
        status_text, icon, color = scan_status(
            latest["Total_Skor"], latest["TWK_Skor"], latest["TIU_Skor"], 
            latest["TKP_Skor"], latest["TWK_Benar"], latest["TIU_Benar"], latest["TKP_P5"]
        )
        
        st.markdown(f"""
        <div style="background-color: {color}; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
            <h3 style="margin:0; color:white;">STATUS PEMINDAI TARGET SKD (TO TERAKHIR): {latest['Nama_TO']}</h3>
            <h1 style="margin:5px 0; font-size: 32px; color:white;">{icon} {status_text}</h1>
            <p style="margin:0; font-size:16px;">Total Skor Terkini: <b>{latest['Total_Skor']} / 550</b> (Target Minimal: 470)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Skor Total SKD", f"{latest['Total_Skor']}", f"{latest['Total_Skor'] - 470} vs Target (470)")
        m2.metric("Skor TWK", f"{latest['TWK_Skor']} (Benar {latest['TWK_Benar']})", f"{latest['TWK_Skor'] - 115} vs Target (115)")
        m3.metric("Skor TIU", f"{latest['TIU_Skor']} (Benar {latest['TIU_Benar']})", f"{latest['TIU_Skor'] - 150} vs Target (150)")
        m4.metric("Skor TKP", f"{latest['TKP_Skor']} (P5: {latest['TKP_P5']})", f"{latest['TKP_Skor'] - 175} vs Target (175)")
        
        st.markdown("---")
        
        # Visual Charts
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("📈 Tren Progres Skor SKD (Per Tryout)")
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=df["Nama_TO"], y=df["Total_Skor"],
                mode='lines+markers', name='Total Skor',
                line=dict(color='#2563EB', width=3),
                marker=dict(size=8)
            ))
            fig_trend.add_trace(go.Scatter(
                x=df["Nama_TO"], y=df["TWK_Skor"],
                mode='lines+markers', name='TWK',
                line=dict(color='#EF4444', dash='dash')
            ))
            fig_trend.add_trace(go.Scatter(
                x=df["Nama_TO"], y=df["TIU_Skor"],
                mode='lines+markers', name='TIU',
                line=dict(color='#F59E0B', dash='dash')
            ))
            fig_trend.add_trace(go.Scatter(
                x=df["Nama_TO"], y=df["TKP_Skor"],
                mode='lines+markers', name='TKP',
                line=dict(color='#10B981', dash='dash')
            ))
            
            # Target Line
            fig_trend.add_hline(y=470, line_dash="dot", line_color="red", annotation_text="Target Target PKN STAN (470)", annotation_position="top right")
            
            fig_trend.update_layout(
                xaxis_title="Tryout",
                yaxis_title="Skor",
                hovermode="x unified",
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with c2:
            st.subheader("📊 Rincian Poin TKP (TO Terakhir)")
            tkp_labels = ['Poin 5', 'Poin 4', 'Poin 3', 'Poin 2', 'Poin 1', 'Poin 0']
            tkp_values = [
                latest['TKP_P5'], latest['TKP_P4'], latest['TKP_P3'],
                latest['TKP_P2'], latest['TKP_P1'], latest['TKP_P0']
            ]
            
            fig_pie = px.pie(
                names=tkp_labels, values=tkp_values,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu_r
            )
            fig_pie.update_layout(margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)

        # Gap Analysis vs Target
        st.subheader("🔍 Diagnostik Subtes vs Benchmark Minimum")
        
        gap_twk = latest['TWK_Skor'] - 115
        gap_tiu = latest['TIU_Skor'] - 150
        gap_tkp = latest['TKP_Skor'] - 175
        
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.markdown(f"**TWK:** {latest['TWK_Skor']} / 115")
            st.progress(min(max(latest['TWK_Skor'] / 150, 0.0), 1.0))
            if gap_twk >= 0:
                st.caption(f"✅ Melampaui target minimal (+{gap_twk} poin)")
            else:
                st.caption(f"❌ Kurang {abs(gap_twk)} poin dari target minimal (Butuh +{abs(gap_twk)//5} soal benar lagi)")

        with col_g2:
            st.markdown(f"**TIU:** {latest['TIU_Skor']} / 150")
            st.progress(min(max(latest['TIU_Skor'] / 175, 0.0), 1.0))
            if gap_tiu >= 0:
                st.caption(f"✅ Melampaui target minimal (+{gap_tiu} poin)")
            else:
                st.caption(f"❌ Kurang {abs(gap_tiu)} poin dari target minimal (Butuh +{abs(gap_tiu)//5} soal benar lagi)")

        with col_g3:
            st.markdown(f"**TKP:** {latest['TKP_Skor']} / 175")
            st.progress(min(max(latest['TKP_Skor'] / 225, 0.0), 1.0))
            if gap_tkp >= 0:
                st.caption(f"✅ Melampaui target minimal (+{gap_tkp} poin)")
            else:
                st.caption(f"❌ Kurang {abs(gap_tkp)} poin dari target minimal")

# ==================== TAB 3: RIWAYAT & KELOLA DATA ====================
with tab3:
    st.subheader("📜 Riwayat Hasil Tryout")
    
    if st.session_state.df_to.empty:
        st.info("Belum ada data tersimpan.")
    else:
        st.dataframe(
            st.session_state.df_to.sort_index(ascending=False),
            use_container_width=True
        )
        
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            # Download Data as CSV
            csv_data = st.session_state.df_to.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Data Riwayat (CSV)",
                data=csv_data,
                file_name="riwayat_skd_stan_2026.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with col_d2:
            if st.button("🗑️ Hapus Semua Data Riwayat", type="primary", use_container_width=True):
                st.session_state.df_to = pd.DataFrame(columns=[
                    "Tanggal", "Nama_TO", "TWK_Benar", "TWK_Salah", "TWK_Skor",
                    "TIU_Benar", "TIU_Salah", "TIU_Skor",
                    "TKP_P5", "TKP_P4", "TKP_P3", "TKP_P2", "TKP_P1", "TKP_P0", "TKP_Skor",
                    "Total_Skor", "Total_Benar", "Total_Salah", "Status"
                ])
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.success("Semua data riwayat berhasil dihapus.")
                st.rerun()
