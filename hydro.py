import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math
import io
import datetime
 
st.set_page_config(
    page_title="Relleno Hidráulico",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=DM+Serif+Display&display=swap');
 
section[data-testid="stSidebar"] {display: none !important;}
div[data-testid="stSidebarNav"]  {display: none !important;}
 
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: #2d1b00 !important;
    background-color: #fdf6ee !important;
}
 
.stApp { background: #fdf6ee !important; }
 
h1 { font-family: 'DM Serif Display', serif !important; font-size: 22px !important; color: #8b3a00 !important; }
h2 { font-family: 'DM Serif Display', serif !important; font-size: 18px !important; color: #8b3a00 !important; }
h3 { font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important; font-size: 15px !important; color: #6b2d00 !important; }
 
.stTabs [data-baseweb="tab-list"] { background: #fff3e6; border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 600 !important;
    color: #8b5e3c !important; border-radius: 8px !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #e8622a !important; color: #fff !important;
    font-weight: 700 !important;
}
 
.hero-banner {
    background: linear-gradient(135deg, #e8622a 0%, #c44a10 60%, #8b3a00 100%);
    border-radius: 14px; padding: 20px 28px; margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(200,80,20,0.25);
}
.hero-banner h1 { color: #fff !important; font-size: 22px !important; margin: 0; }
.hero-banner p  { color: #ffd5b5 !important; font-size: 13px !important; margin: 4px 0 0 0; }
 
.metric-card {
    background: #fff; border: 1px solid #f0d5c0; border-radius: 12px;
    padding: 14px 18px; margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(180,80,20,0.08);
}
.metric-label { color: #a05030; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-value { color: #8b3a00; font-size: 22px; font-weight: 700; font-family: 'DM Serif Display', serif; }
.metric-unit  { color: #c07050; font-size: 12px; }
 
.result-highlight {
    background: linear-gradient(135deg, #fff8f3, #ffe8d6);
    border: 2px solid #e8622a; border-radius: 10px;
    padding: 12px 18px; margin: 10px 0;
    box-shadow: 0 2px 10px rgba(232,98,42,0.15);
}
.result-highlight .label { color: #8b3a00; font-weight: 700; font-size: 13px; }
.result-highlight .value { color: #e8622a; font-size: 20px; font-weight: 700; }
 
.stDataFrame { border-radius: 8px; overflow: hidden; }
div[data-testid="stNumberInput"] label { color: #6b2d00 !important; font-weight: 600 !important; }
div[data-testid="stSelectbox"] label { color: #6b2d00 !important; font-weight: 600 !important; }
 
.section-header {
    background: #fff3e6; border-left: 4px solid #e8622a;
    padding: 8px 14px; border-radius: 0 8px 8px 0;
    margin: 16px 0 10px 0;
    font-weight: 700; color: #8b3a00; font-size: 15px;
}
 
.info-box {
    background: #fff8f0; border: 1px solid #f5c99a;
    border-radius: 8px; padding: 10px 14px;
    color: #7a4010; font-size: 13px;
}
 
.styled-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.styled-table th {
    background: #8b3a00; color: #fff; padding: 8px 12px;
    text-align: left; font-weight: 600; font-size: 12px;
    text-transform: uppercase; letter-spacing: 0.03em;
}
.styled-table td {
    padding: 7px 12px; border-bottom: 1px solid #f0d5c0;
    color: #3d1a00;
}
.styled-table tr:nth-child(even) td { background: #fff8f3; }
.styled-table tr:hover td { background: #ffe8d6; }
 
.stButton > button {
    background: linear-gradient(135deg, #e8622a, #c44a10) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 10px 20px !important;
}
.stButton > button:hover { opacity: 0.9 !important; }
 
div[data-testid="stInfo"] { background: #fff8f0 !important; color: #7a4010 !important; border-color: #f5c99a !important; }
div[data-testid="stSuccess"] { background: #f0fff4 !important; color: #1a5c2a !important; border-color: #86efac !important; }
div[data-testid="stWarning"] { background: #fffbeb !important; color: #7c5600 !important; border-color: #fcd34d !important; }
</style>
""", unsafe_allow_html=True)
 
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#fffaf5",
    plot_bgcolor="#fff8f3",
    font=dict(family="DM Sans, sans-serif", color="#3d1a00", size=13),
    xaxis=dict(gridcolor="#f0d5c0", linecolor="#e0b090", tickfont=dict(size=12)),
    yaxis=dict(gridcolor="#f0d5c0", linecolor="#e0b090", tickfont=dict(size=12)),
    legend=dict(font=dict(size=12), bgcolor="rgba(255,248,240,0.9)", bordercolor="#f0d5c0", borderwidth=1),
    margin=dict(l=55, r=35, t=55, b=55),
)
WARM_COLORS = ["#e8622a", "#c44a10", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"]
 
def render_table(df):
    rows = "".join(
        f"<tr>{''.join(f'<td>{v}</td>' for v in row)}</tr>"
        for _, row in df.iterrows()
    )
    headers = "".join(f"<th>{c}</th>" for c in df.columns)
    return f'<table class="styled-table"><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>'
 
def metric_card(label, value, unit=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value} <span class="metric-unit">{unit}</span></div>
    </div>"""
 
def result_highlight(label, value):
    return f"""
    <div class="result-highlight">
        <div class="label">📌 {label}</div>
        <div class="value">{value}</div>
    </div>"""
 
def section_hdr(txt):
    st.markdown(f'<div class="section-header">⬧ {txt}</div>', unsafe_allow_html=True)
 
def generate_template_csv() -> bytes:
    out = io.StringIO()
    out.write("# CSV MAESTRO - RELLENO HIDRAULICO\n#\n")
    out.write("SECCION,RELAVE\nParametro,Valor\n")
    for r in [("GE_relave",2.49),("d80_micrones",75),("pH",7.2),
              ("pct_azufre",0.23),("pct_arsenico",0.12)]:
        out.write(f"{r[0]},{r[1]}\n")
    out.write("#\nSECCION,PULPA\nParametro,Valor\n")
    for r in [("SGm_pulpa",1.49),("Cw_pct_solidos_peso",25.0),
              ("caudal_litros",232),("tiempo_seg",36.45)]:
        out.write(f"{r[0]},{r[1]}\n")
    out.write("#\nSECCION,MEZCLA\nMezcla,Cemento_kg,Relave_kg,Agua_kg,Aditivos_kg\n")
    for r in [["M1",150,1860.03,180,2.28],["M2",200,1822.03,180,4.4],["M3",250,1779.54,180,4.4]]:
        out.write(",".join(str(v) for v in r)+"\n")
    out.write("#\nSECCION,UCS\nEspecimen,Dia7_MPa,Dia14_MPa,Dia28_MPa\n")
    for r in [["CASO_A",0.136,0.186,0.191],["CASO_B",0.226,0.352,0.422],["CASO_C",0.141,0.180,0.215],
              ["CASO_1.1",0.956,1.24,1.304],["CASO_1.2",1.501,1.715,1.807],
              ["CASO_1.3",0.212,0.358,0.384],["CASO_1.4",2.504,2.894,3.015],
              ["CASO_1.5",1.308,1.594,1.625]]:
        out.write(",".join(str(v) for v in r)+"\n")
    out.write("#\nSECCION,CASERON\nParametro,Valor\n")
    for r in [("longitud_m",17.7),("ancho_m",12.5),("altura_m",5.0),
              ("densidad_RH_tm3",2.22),("angulo_friccion_deg",32.0),
              ("humedad_relave_pct",22.62),("absorcion_pct",20.0)]:
        out.write(f"{r[0]},{r[1]}\n")
    return out.getvalue().encode("utf-8")
 
def parse_master_csv(uploaded_file) -> dict:
    content = uploaded_file.read().decode("utf-8")
    sections, current_section, current_rows, header = {}, None, [], None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if line.upper().startswith("SECCION,"):
            if current_section and header and current_rows:
                sections[current_section] = pd.DataFrame(current_rows, columns=header)
            current_section = line.split(",",1)[1].strip().upper()
            current_rows, header = [], None
            continue
        parts = line.split(",")
        if header is None:
            header = parts
        else:
            parsed = []
            for v in parts:
                try: parsed.append(float(v) if "." in v else int(v))
                except ValueError: parsed.append(v.strip())
            current_rows.append(parsed)
    if current_section and header and current_rows:
        sections[current_section] = pd.DataFrame(current_rows, columns=header)
    return sections
 
DEFAULT_RELAVE = {
    "GE_relave": 2.49, "d80_micrones": 75, "pH": 7.2,
    "pct_azufre": 0.23, "pct_arsenico": 0.12,
}
DEFAULT_PULPA = {
    "SGm_pulpa": 1.49, "Cw_pct_solidos_peso": 25.0,
    "caudal_litros": 232, "tiempo_seg": 36.45,
}
DEFAULT_CASERON = {
    "longitud_m": 17.7, "ancho_m": 12.5, "altura_m": 5.0,
    "densidad_RH_tm3": 2.22, "angulo_friccion_deg": 32.0,
    "humedad_relave_pct": 22.62, "absorcion_pct": 20.0,
}
DEFAULT_MEZCLAS = pd.DataFrame({
    "Mezcla": ["M1", "M2", "M3"],
    "Cemento_kg": [150.0, 200.0, 250.0],
    "Relave_kg": [1860.03, 1822.03, 1779.54],
    "Agua_kg": [180.0, 180.0, 180.0],
    "Aditivos_kg": [2.28, 4.4, 4.4],
})
DEFAULT_UCS = pd.DataFrame({
    "Especimen": ["CASO_A","CASO_B","CASO_C","CASO_1.1","CASO_1.2","CASO_1.3","CASO_1.4","CASO_1.5"],
    "Dia7_MPa":  [0.136,0.226,0.141,0.956,1.501,0.212,2.504,1.308],
    "Dia14_MPa": [0.186,0.352,0.180,1.240,1.715,0.358,2.894,1.594],
    "Dia28_MPa": [0.191,0.422,0.215,1.304,1.807,0.384,3.015,1.625],
})
 
if "csv_activo" not in st.session_state: st.session_state.csv_activo = False
if "relave"  not in st.session_state: st.session_state.relave  = DEFAULT_RELAVE.copy()
if "pulpa"   not in st.session_state: st.session_state.pulpa   = DEFAULT_PULPA.copy()
if "caseron" not in st.session_state: st.session_state.caseron = DEFAULT_CASERON.copy()
if "mezclas_df" not in st.session_state: st.session_state.mezclas_df = DEFAULT_MEZCLAS.copy()
if "ucs_df"     not in st.session_state: st.session_state.ucs_df     = DEFAULT_UCS.copy()
 
st.markdown("""
<div class="hero-banner">
  <h1>💧 Relleno Hidráulico (RH)</h1>
  <p>Análisis técnico · Diseño de mezcla · Cálculos geomecánicos </p>
</div>
""", unsafe_allow_html=True)
 
st.markdown("### 📂 Carga de Datos Maestros")
col_info, col_dl = st.columns([3, 1])
with col_info:
    st.info("**Paso 1:** Descargue la plantilla CSV → **Paso 2:** Complete sus datos → **Paso 3:** Suba el archivo aquí.")
with col_dl:
    st.download_button("⬇️ Descargar Plantilla", data=generate_template_csv(),
        file_name="plantilla_RH_maestro.csv", mime="text/csv", use_container_width=True)
 
uploaded_csv = st.file_uploader("Seleccionar archivo CSV maestro (.csv)", type=["csv"], key="master_csv")
if uploaded_csv is not None:
    try:
        sections = parse_master_csv(uploaded_csv)
 
        def load_kv(sec, default):
            if sec not in sections: return default.copy()
            df_ = sections[sec].copy()
            df_.columns = ["Parametro", "Valor"]
            d = default.copy()
            for _, r in df_.iterrows():
                k = str(r["Parametro"]).strip()
                if k in d: d[k] = float(r["Valor"])
            return d
 
        st.session_state.relave  = load_kv("RELAVE",  DEFAULT_RELAVE)
        st.session_state.pulpa   = load_kv("PULPA",   DEFAULT_PULPA)
        st.session_state.caseron = load_kv("CASERON", DEFAULT_CASERON)
 
        if "MEZCLA" in sections:
            dm = sections["MEZCLA"].copy()
            dm.columns = ["Mezcla","Cemento_kg","Relave_kg","Agua_kg","Aditivos_kg"]
            for col in dm.columns[1:]: dm[col] = pd.to_numeric(dm[col], errors="coerce")
            st.session_state.mezclas_df = dm.reset_index(drop=True)
 
        if "UCS" in sections:
            du = sections["UCS"].copy()
            du.columns = ["Especimen","Dia7_MPa","Dia14_MPa","Dia28_MPa"]
            for col in du.columns[1:]: du[col] = pd.to_numeric(du[col], errors="coerce")
            st.session_state.ucs_df = du.reset_index(drop=True)
 
        st.session_state.csv_activo = True
        st.success(f"✔ CSV cargado correctamente — secciones: {', '.join(sections.keys())}")
    except Exception as e:
        st.error(f"❌ Error al procesar el CSV: {e}")
 
if st.session_state.csv_activo:
    if st.button("🔄 Restaurar datos por defecto"):
        for k in ["csv_activo","relave","pulpa","caseron","mezclas_df","ucs_df"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
 
st.markdown("---")
 
tabs = st.tabs([
    "🔬 Propiedades del Relave",
    "⚗️ Diseño de Mezcla",
    "💪 Resistencias UCS",
    "🌊 Pulpa Hidráulica",
    "📐 Geomecánica",
])
 
with tabs[0]:
    st.markdown("## Propiedades Físicas del Relave")
    relave = st.session_state.relave
    pulpa  = st.session_state.pulpa
 
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(metric_card("Gravedad Específica", f"{relave['GE_relave']:.2f}", "—"), unsafe_allow_html=True)
    with m2: st.markdown(metric_card("d80", f"{relave['d80_micrones']:.0f}", "μm"), unsafe_allow_html=True)
    with m3: st.markdown(metric_card("pH", f"{relave['pH']:.1f}", "—"), unsafe_allow_html=True)
    with m4:
        Q = (pulpa["caudal_litros"] / pulpa["tiempo_seg"]) * 86400 / 1000
        st.markdown(metric_card("Caudal estimado", f"{Q:.1f}", "m³/día"), unsafe_allow_html=True)
 
    section_hdr("Gravedad Específica por Picnómetro")
    c1, c2 = st.columns(2)
    with c1:
        df_pico = pd.DataFrame({
            "Ensayo": ["GE Relave (promedio)","% Azufre (FRX)","% Arsénico (FRX)"],
            "Valor": [f"{relave['GE_relave']:.2f}",
                      f"{relave['pct_azufre']:.2f}%",
                      f"{relave['pct_arsenico']:.2f}%"],
        })
        st.markdown(render_table(df_pico), unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="info-box">
        <b>Notas de clasificación:</b><br>
        • pH {relave['pH']:.1f} → Intermedio (7–7.5)<br>
        • Azufre {relave['pct_azufre']:.2f}% → Cemento Portland HE recomendado<br>
        • Arsénico {relave['pct_arsenico']:.2f}% → Monitorear lixiviado<br>
        • GE {relave['GE_relave']:.2f} → Relave típico de sulfuros
        </div>
        """, unsafe_allow_html=True)
 
    section_hdr("Porcentaje de Sólidos en Pulpa — Balanza Marcy")
 
    Cw_m = float(pulpa["Cw_pct_solidos_peso"])
    SGm  = float(pulpa["SGm_pulpa"])
    SGs  = float(relave["GE_relave"])
    Cv   = Cw_m * (SGm / SGs)
 
    c3, c4 = st.columns(2)
    with c3:
        df_marcy = pd.DataFrame({
            "Parámetro": ["% Sólidos en peso (Cw)","SGm pulpa","GE relave (SGs)","% Sólidos en volumen (Cv)"],
            "Valor": [f"{Cw_m:.2f}%", f"{SGm:.2f}", f"{SGs:.2f}", f"{Cv:.2f}%"],
        })
        st.markdown(render_table(df_marcy), unsafe_allow_html=True)
    with c4:
        t_sed = [0,3,6,9,12,15,18,24,36,39,42,45,48,60,90,120,300,600,1020]
        h_sed = [35,33.8,32.9,32.3,31.1,30.6,30,29.2,27.3,26.8,26.2,25.9,25.65,23.5,19.3,15.8,14.5,10.61,9.55]
        fig_sed = go.Figure()
        fig_sed.add_trace(go.Scatter(
            x=t_sed, y=h_sed, mode="lines+markers",
            line=dict(color="#e8622a", width=2.5),
            marker=dict(color="#c44a10", size=6),
            name="Altura sedimentación"
        ))
        fig_sed.update_layout(**PLOTLY_LAYOUT, height=280,
            title=dict(text="Velocidad de Sedimentación", font=dict(size=14)),
            xaxis_title="Tiempo (min)", yaxis_title="H (cm)")
        st.plotly_chart(fig_sed, use_container_width=True)
 
    section_hdr("Granulometría del Relave — ASTM D 421-58")
    mallas_diam = [600,425,300,250,212,180,150,106,75,60,50,38]
    pasado_pct  = [99.78,99.61,99.33,98.25,97.07,96.60,93.67,83.35,82.17,78.66,74.17,73.30]
 
    fig_gran = go.Figure()
    fig_gran.add_trace(go.Scatter(
        x=mallas_diam, y=pasado_pct, mode="lines+markers",
        line=dict(color="#e8622a", width=2.5),
        marker=dict(color="#c44a10", size=7),
        fill="tozeroy", fillcolor="rgba(232,98,42,0.1)",
        name="% Pasado acumulado"
    ))
    fig_gran.add_vline(x=75, line_dash="dash", line_color="#f59e0b",
                       annotation_text="d80=75μm", annotation_font_color="#8b3a00")
    fig_gran.update_layout(**PLOTLY_LAYOUT, height=320,
        title=dict(text="Curva Granulométrica del Relave", font=dict(size=14)),
        xaxis_title="Diámetro (μm)", yaxis_title="% Pasado Acumulado",
        )
    st.plotly_chart(fig_gran, use_container_width=True)
 
 
with tabs[1]:
    st.markdown("## Diseño del Relleno Hidráulico — Dosificaciones")
    mezclas = st.session_state.mezclas_df.copy()
    caseron = st.session_state.caseron
 
    mezclas["Total_kg"] = (mezclas["Cemento_kg"] + mezclas["Relave_kg"] +
                           mezclas["Agua_kg"] + mezclas["Aditivos_kg"])
    mezclas["Densidad_kgm3"] = mezclas["Total_kg"].round(2)
 
    section_hdr("Dosificaciones Teóricas")
    for _, row in mezclas.iterrows():
        with st.expander(f"📋 {row['Mezcla']} — Cemento: {row['Cemento_kg']:.0f} kg/m³", expanded=True):
            ca, cb = st.columns(2)
            with ca:
                df_mix = pd.DataFrame({
                    "Componente": ["Cemento","Relave","Agua","Aditivos","TOTAL"],
                    "Peso (kg)": [row["Cemento_kg"], row["Relave_kg"], row["Agua_kg"],
                                  row["Aditivos_kg"], row["Total_kg"]],
                })
                df_mix["Peso (kg)"] = df_mix["Peso (kg)"].apply(lambda x: f"{x:.2f}")
                st.markdown(render_table(df_mix), unsafe_allow_html=True)
            with cb:
                w_pct  = float(caseron["humedad_relave_pct"])
                ab_pct = float(caseron["absorcion_pct"])
                rl_orig = float(row["Relave_kg"])
                rl_corr = rl_orig * (1 + (w_pct - ab_pct) / 100)
                agua_corr = float(row["Agua_kg"]) - rl_orig * ((w_pct - ab_pct) / 100)
                df_corr = pd.DataFrame({
                    "Componente": ["Cemento","Relave (corr.)","Agua (corr.)","Aditivos","TOTAL"],
                    "Peso corr. (kg)": [f"{row['Cemento_kg']:.2f}",
                                        f"{rl_corr:.2f}", f"{agua_corr:.2f}",
                                        f"{row['Aditivos_kg']:.2f}",
                                        f"{row['Cemento_kg']+rl_corr+agua_corr+row['Aditivos_kg']:.2f}"],
                })
                st.markdown(f"**Corrección por humedad** (w={w_pct}%, abs={ab_pct}%)", unsafe_allow_html=False)
                st.markdown(render_table(df_corr), unsafe_allow_html=True)
 
    section_hdr("Proporciones por Mezcla (kg/m³)")
    fig_comp = go.Figure()
    for i, comp in enumerate(["Cemento_kg","Relave_kg","Agua_kg","Aditivos_kg"]):
        fig_comp.add_trace(go.Bar(
            name=comp.replace("_kg",""),
            x=mezclas["Mezcla"],
            y=mezclas[comp],
            marker_color=WARM_COLORS[i],
            text=mezclas[comp].apply(lambda x: f"{x:.0f}"),
            textposition="inside",
            textfont=dict(size=12, color="white"),
        ))
    fig_comp.update_layout(**PLOTLY_LAYOUT, barmode="stack", height=380,
        title=dict(text="Composición de Mezclas por Componente", font=dict(size=14)),
        )
    st.plotly_chart(fig_comp, use_container_width=True)
 
    section_hdr("Selección de Cemento")
    ca, cb = st.columns(2)
    with ca:
        df_cem = pd.DataFrame({
            "Propiedad": ["Densidad","Fraguado inicial","Fraguado final","Resist. 28d"],
            "Portland HE": ["2930 kg/m³","110–140 min","190–240 min","25–30 MPa"],
            "Portland GU": ["2930 kg/m³","140–160 min","200–240 min","28–30 MPa"],
        })
        st.markdown(render_table(df_cem), unsafe_allow_html=True)
    with cb:
        st.markdown("""
        <div class="info-box">
        <b>Criterio de selección:</b><br>
        • <b>Portland HE</b>: Resistencia moderada a sulfatos, recomendado cuando el % azufre es moderado.<br>
        • <b>Portland GU</b>: Alta resistencia inicial, ideal para recuperaciones rápidas de cámara.<br>
        • Ambos alcanzan 25–30 MPa a los 28 días.
        </div>
        """, unsafe_allow_html=True)
 
 
with tabs[2]:
    st.markdown("## Curvas de Resistencia a la Compresión Simple (UCS)")
    ucs_df = st.session_state.ucs_df.copy()
 
    section_hdr("Tabla de Resultados UCS")
    df_show = ucs_df.copy()
    df_show.columns = ["Especimen","Día 7 (MPa)","Día 14 (MPa)","Día 28 (MPa)"]
    st.markdown(render_table(df_show), unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    section_hdr("Curva de Resistencia — Prueba de Curado")
    fig_ucs = go.Figure()
    dias = [7, 14, 28]
    for i, (_, row) in enumerate(ucs_df.iterrows()):
        vals = [row["Dia7_MPa"], row["Dia14_MPa"], row["Dia28_MPa"]]
        color = WARM_COLORS[i % len(WARM_COLORS)]
        fig_ucs.add_trace(go.Scatter(
            x=dias, y=vals, mode="lines+markers",
            name=row["Especimen"],
            line=dict(color=color, width=2.5),
            marker=dict(size=9, color=color, line=dict(color="white", width=1.5)),
        ))
    fig_ucs.update_layout(**PLOTLY_LAYOUT, height=420,
        title=dict(text="Curva de Resistencia / Prueba de Curado — Todos los Especímenes", font=dict(size=14)),
        yaxis_title="UCS (MPa)")
    st.plotly_chart(fig_ucs, use_container_width=True)
 
    section_hdr("Comparativa a 28 días")
    fig_28 = go.Figure()
    fig_28.add_trace(go.Bar(
        x=ucs_df["Especimen"],
        y=ucs_df["Dia28_MPa"],
        marker_color=[WARM_COLORS[i % len(WARM_COLORS)] for i in range(len(ucs_df))],
        text=ucs_df["Dia28_MPa"].apply(lambda x: f"{x:.3f}"),
        textposition="outside",
        textfont=dict(size=12),
    ))
    fig_28.update_layout(**PLOTLY_LAYOUT, height=360,
        title=dict(text="Resistencia a 28 días por Especímen", font=dict(size=14)))
    st.plotly_chart(fig_28, use_container_width=True)
 
 
with tabs[3]:
    st.markdown("## Pulpa de Relleno Hidráulico")
    pulpa  = st.session_state.pulpa
    relave = st.session_state.relave
 
    section_hdr("Concentración Volumétrica de Sólidos")
 
    SGm = float(pulpa["SGm_pulpa"])
    SGs = float(relave["GE_relave"])
    Cw  = float(pulpa["Cw_pct_solidos_peso"]) / 100.0
 
    Cv = Cw * (SGm / SGs)
 
    mu_L = 0.001
    Cv_frac = Cv
    if Cw > 1:
        Cw_frac = Cw / 100
        Cv_frac = Cw_frac * (SGm / SGs)
    else:
        Cv_frac = Cv
 
    try:
        mu_m = mu_L * (math.exp(-10.4 * Cv_frac)) / ((1 - Cv_frac / 0.62) ** 8)
    except:
        mu_m = 0.0
 
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(metric_card("Cv (sólidos volumen)", f"{Cv_frac*100:.2f}", "%"), unsafe_allow_html=True)
    with c2: st.markdown(metric_card("Viscosidad μm", f"{mu_m:.4f}", "Pa·s"), unsafe_allow_html=True)
    with c3:
        Q_m3d = (float(pulpa["caudal_litros"]) / float(pulpa["tiempo_seg"])) * 86400 / 1000
        st.markdown(metric_card("Caudal RH", f"{Q_m3d:.1f}", "m³/día"), unsafe_allow_html=True)
 
    ca, cb = st.columns(2)
    with ca:
        section_hdr("Parámetros de Pulpa")
        df_pulpa = pd.DataFrame({
            "Parámetro": ["SGm (pulpa)","SGs (relave)","Cw (% en peso)","Cv (% en volumen)",
                          "μL agua (Pa·s)","μm pulpa (Pa·s)"],
            "Valor": [f"{SGm:.3f}",f"{SGs:.3f}",
                      f"{float(pulpa['Cw_pct_solidos_peso']):.2f}%",
                      f"{Cv_frac*100:.2f}%",
                      f"{mu_L:.4f}",f"{mu_m:.4f}"],
        })
        st.markdown(render_table(df_pulpa), unsafe_allow_html=True)
 
        st.markdown(result_highlight("Viscosidad dinámica μm", f"{mu_m:.4f} Pa·s"), unsafe_allow_html=True)
        st.markdown(result_highlight("% Sólidos en Volumen (Cv)", f"{Cv_frac*100:.2f} %"), unsafe_allow_html=True)
 
    with cb:
        section_hdr("Fluidez de la Pulpa")
        phi_prom = st.number_input("Ø promedio mesa de flujo (mm)", value=230.0, step=1.0)
        phi_inf  = st.number_input("Ø inferior molde (mm)", value=101.6, step=0.1)
        fluidez  = ((phi_prom - phi_inf) / phi_inf) * 100
 
        df_fl = pd.DataFrame({
            "Parámetro": ["Ø promedio (mm)","Ø inferior (mm)","% Fluidez"],
            "Valor": [f"{phi_prom:.1f}", f"{phi_inf:.1f}", f"{fluidez:.2f}%"],
        })
        st.markdown(render_table(df_fl), unsafe_allow_html=True)
        st.markdown(result_highlight("% Fluidez calculado", f"{fluidez:.2f} %"), unsafe_allow_html=True)
 
        st.markdown("""
        <div class="info-box" style="margin-top:10px;">
        <b>Ecuación de Wellman:</b><br>
        μm = μL × exp(−10.4·Cv) / (1 − Cv/0.62)⁸<br><br>
        <b>Concentración volumétrica:</b><br>
        Cv = Cw × (SGm / SGs)
        </div>
        """, unsafe_allow_html=True)
 
    section_hdr("Sensibilidad: Viscosidad vs % Sólidos en Volumen")
    cv_arr = np.linspace(0.05, 0.58, 80)
    mu_arr = []
    for cv_i in cv_arr:
        try:
            mu_i = mu_L * (math.exp(-10.4 * cv_i)) / ((1 - cv_i / 0.62) ** 8)
            mu_arr.append(mu_i)
        except:
            mu_arr.append(np.nan)
 
    fig_visc = go.Figure()
    fig_visc.add_trace(go.Scatter(
        x=cv_arr * 100, y=mu_arr,
        mode="lines", line=dict(color="#e8622a", width=3),
        name="μm (Pa·s)"
    ))
    fig_visc.add_vline(x=Cv_frac * 100, line_dash="dash", line_color="#f59e0b",
                       annotation_text=f"Cv={Cv_frac*100:.1f}%", annotation_font_color="#8b3a00")
    fig_visc.update_layout(**PLOTLY_LAYOUT, height=320,
        title=dict(text="Viscosidad Dinámica vs % Sólidos en Volumen", font=dict(size=14)),
        xaxis_title="Cv (%)", yaxis_title="μm (Pa·s)")
    st.plotly_chart(fig_visc, use_container_width=True)
 
 
with tabs[4]:
    st.markdown("## Cálculos Geomecánicos del Caserón")
    caseron = st.session_state.caseron
 
    L   = float(caseron["longitud_m"])
    W   = float(caseron["ancho_m"])
    H   = float(caseron["altura_m"])
    gRH = float(caseron["densidad_RH_tm3"])
    phi = float(caseron["angulo_friccion_deg"])
 
    section_hdr("Parámetros del Caserón")
    ca, cb = st.columns(2)
    with ca:
        df_geo = pd.DataFrame({
            "Parámetro": ["Longitud L (m)","Ancho W (m)","Altura H (m)","γ RH (t/m³)","φ fricción (°)"],
            "Valor": [f"{L:.1f}",f"{W:.1f}",f"{H:.1f}",f"{gRH:.2f}",f"{phi:.1f}"],
        })
        st.markdown(render_table(df_geo), unsafe_allow_html=True)
    with cb:
        caso = "A (W ≥ H)" if W >= H else "B (W < H)"
        st.markdown(f"""
        <div class="info-box">
        <b>Configuración detectada:</b><br>
        W = {W:.1f} m &nbsp;|&nbsp; H = {H:.1f} m<br>
        → <b>Caso {caso}</b><br><br>
        Las ecuaciones de resistencia requerida (UCS_RH) varían según si el ancho
        es mayor o menor que la altura del caserón.
        </div>
        """, unsafe_allow_html=True)
 
    section_hdr("Resistencia Requerida — UCS_RH (Mitchell)")
    if W >= H:
        UCS_RH = (L * gRH * (2 * H - W)) / (2 * (H + L) - W)
        formula = "UCS_RH = L·γ·(2H − W) / [2(H + L) − W]"
    else:
        UCS_RH = (gRH * H) / (1 - H / L)
        formula = "UCS_RH = γ·H / (1 − H/L)"
 
    alpha = 45 + phi / 2
    alpha_rad = math.radians(alpha)
    cohesion = (gRH * H) / (2 * (H / L + math.tan(alpha_rad)))
    Wn = W * H * (gRH * L - 2 * cohesion)
 
    c3, c4 = st.columns(2)
    with c3:
        df_res = pd.DataFrame({
            "Concepto": ["Caso geométrico","Fórmula UCS","UCS_RH (MPa)","α falla (°)","Cohesión c (MPa)"],
            "Valor": [f"Caso {caso}", formula, f"{UCS_RH:.4f}", f"{alpha:.1f}", f"{cohesion:.4f}"],
        })
        st.markdown(render_table(df_res), unsafe_allow_html=True)
        st.markdown(result_highlight("UCS_RH requerido", f"{UCS_RH:.2f} MPa"), unsafe_allow_html=True)
    with c4:
        df_cun = pd.DataFrame({
            "Concepto": ["φ' fricción (°)","α falla (°)","γ RH (t/m³)","H caserón (m)","Wn cuña (t)"],
            "Valor": [f"{phi:.1f}",f"{alpha:.1f}",f"{gRH:.2f}",f"{H:.1f}",f"{Wn:.1f}"],
        })
        st.markdown(render_table(df_cun), unsafe_allow_html=True)
        st.markdown(result_highlight("Peso cuña Wn", f"{Wn:.1f} t"), unsafe_allow_html=True)
 
    section_hdr("Verificación contra UCS Ensayado")
    ucs_df = st.session_state.ucs_df.copy()
    ucs_max = float(ucs_df["Dia28_MPa"].max())
    ucs_min = float(ucs_df["Dia28_MPa"].min())
    ucs_mean= float(ucs_df["Dia28_MPa"].mean())
 
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(metric_card("UCS requerido", f"{UCS_RH:.3f}", "MPa"), unsafe_allow_html=True)
    with m2: st.markdown(metric_card("UCS máx. 28d", f"{ucs_max:.3f}", "MPa"), unsafe_allow_html=True)
    with m3: st.markdown(metric_card("UCS promedio 28d", f"{ucs_mean:.3f}", "MPa"), unsafe_allow_html=True)
    with m4:
        factor = ucs_mean / UCS_RH if UCS_RH > 0 else 0
        color_ok = "✅" if factor >= 1.0 else "⚠️"
        st.markdown(metric_card(f"{color_ok} Factor UCS_ensayado/UCS_req", f"{factor:.2f}", "—"), unsafe_allow_html=True)
 
    section_hdr("Gráfico Geomecánico — Distribución de Presiones")
    z_arr = np.linspace(0, H, 60)
    pv_arr = gRH * z_arr
 
    fig_geo = go.Figure()
    fig_geo.add_trace(go.Scatter(
        x=pv_arr, y=z_arr,
        mode="lines", fill="tozerox",
        fillcolor="rgba(232,98,42,0.15)",
        line=dict(color="#e8622a", width=3),
        name="Presión vertical γ·z"
    ))
    fig_geo.add_vline(x=UCS_RH, line_dash="dash", line_color="#10b981",
                      annotation_text=f"UCS_RH={UCS_RH:.2f} MPa",
                      annotation_font_color="#1a5c2a")
    fig_geo.update_layout(**PLOTLY_LAYOUT, height=380,
        title=dict(text="Distribución de Presión Vertical en el Relleno", font=dict(size=14)))
    st.plotly_chart(fig_geo, use_container_width=True)
 
    section_hdr("Comparativa UCS 28 días vs Requerimiento")
    especimenes = ucs_df["Especimen"].tolist()
    vals_28     = ucs_df["Dia28_MPa"].tolist()
    colores     = ["#10b981" if v >= UCS_RH else "#e8622a" for v in vals_28]
 
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        x=especimenes, y=vals_28,
        marker_color=colores,
        text=[f"{v:.3f}" for v in vals_28],
        textposition="outside",
        textfont=dict(size=12),
        name="UCS 28d"
    ))
    fig_comp.add_hline(y=UCS_RH, line_dash="dash", line_color="#f59e0b", line_width=2.5,
                       annotation_text=f"UCS_RH requerido = {UCS_RH:.3f} MPa",
                       annotation_font_color="#8b3a00", annotation_font_size=12)
    fig_comp.update_layout(**PLOTLY_LAYOUT, height=360,
        title=dict(text="UCS a 28 días — Verde: cumple, Naranja: no cumple", font=dict(size=14)))
    st.plotly_chart(fig_comp, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════
    #  REPORTE PDF — GEOMECÁNICA
    # ══════════════════════════════════════════════════════════════════
    section_hdr("📄 Exportar Reporte Geomecánico")
    st.markdown("""
    <div class="info-box">
    Genera un reporte PDF completo con todos los parámetros, tablas de resultados
    y gráficos de esta sección (Distribución de Presiones y Comparativa UCS 28d).
    </div>
    """, unsafe_allow_html=True)

    if st.button("📥 Generar Reporte PDF — Geomecánica", use_container_width=True):
        import io as _io
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        Table, TableStyle, Image as RLImage,
                                        HRFlowable, KeepTogether)
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

        # ── helper: Plotly fig → ReportLab Image ──────────────────────
        def fig_to_rli(fig, w_cm=15.5, h_cm=8.5):
            buf = _io.BytesIO()
            fig.write_image(buf, format="png", width=950, height=520, scale=2)
            buf.seek(0)
            return RLImage(buf, width=w_cm*cm, height=h_cm*cm)

        # ── Layout para exportar (fondo blanco) ───────────────────────
        LP = dict(
            paper_bgcolor="white", plot_bgcolor="#f5f5f5",
            font=dict(family="Arial, sans-serif", color="#2d1b00", size=13),
            margin=dict(l=55, r=35, t=60, b=55),
        )

        # Gráfico 1 — Distribución de Presiones
        fig_g1 = go.Figure()
        fig_g1.add_trace(go.Scatter(
            x=pv_arr, y=z_arr, mode="lines", fill="tozerox",
            fillcolor="rgba(232,98,42,0.2)",
            line=dict(color="#e8622a", width=3),
            name="Presión vertical (t/m²)"
        ))
        fig_g1.add_vline(x=UCS_RH, line_dash="dash", line_color="#10b981",
                         annotation_text=f"UCS_RH = {UCS_RH:.3f} MPa",
                         annotation_font_color="#1a7a40")
        fig_g1.update_layout(**LP, height=520,
            title=dict(text="Distribución de Presión Vertical en el Relleno", font=dict(size=15)),
            xaxis_title="Presión vertical γ·z (t/m²)", yaxis_title="Profundidad z (m)")

        # Gráfico 2 — Barras UCS 28d
        fig_g2 = go.Figure()
        fig_g2.add_trace(go.Bar(
            x=especimenes, y=vals_28, marker_color=colores,
            text=[f"{v:.3f}" for v in vals_28], textposition="outside",
            name="UCS 28d (MPa)"
        ))
        fig_g2.add_hline(y=UCS_RH, line_dash="dash", line_color="#f59e0b", line_width=2.5,
                         annotation_text=f"UCS_RH req. = {UCS_RH:.3f} MPa",
                         annotation_font_color="#8b3a00")
        fig_g2.update_layout(**LP, height=520,
            title=dict(text="UCS a 28 días por Especimen vs Requerimiento", font=dict(size=15)),
            yaxis_title="UCS (MPa)")

        # ── Estilos ReportLab ──────────────────────────────────────────
        styles = getSampleStyleSheet()

        def ps(name, base="Normal", **kw):
            return ParagraphStyle(name, parent=styles[base], **kw)

        S_TITLE = ps("rh_title", "Title", fontSize=20,
                     textColor=colors.HexColor("#8b3a00"),
                     fontName="Helvetica-Bold", spaceAfter=2)
        S_SUB   = ps("rh_sub", fontSize=10,
                     textColor=colors.HexColor("#b07050"),
                     fontName="Helvetica-Oblique", spaceAfter=10)
        S_H2    = ps("rh_h2", fontSize=12,
                     textColor=colors.HexColor("#7a2e00"),
                     fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=5)
        S_BODY  = ps("rh_body", fontSize=9.5,
                     textColor=colors.HexColor("#3d1a00"),
                     fontName="Helvetica", leading=14)
        S_NOTE  = ps("rh_note", fontSize=8.5,
                     textColor=colors.HexColor("#7a4010"),
                     fontName="Helvetica-Oblique", leading=12)
        S_RIGHT = ps("rh_right", fontSize=8,
                     textColor=colors.HexColor("#a06040"),
                     fontName="Helvetica", alignment=TA_RIGHT)

        # ── Estilo de tabla ────────────────────────────────────────────
        TS = TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#8b3a00")),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0), 9),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1),
             [colors.HexColor("#fff8f3"), colors.white]),
            ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",      (0, 1), (-1, -1), 9),
            ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#e0c0a0")),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ])

        def make_tbl(rows, col_w=None):
            t = Table(rows, colWidths=col_w)
            t.setStyle(TS)
            return t

        def hr():
            return HRFlowable(width="100%", thickness=1.5,
                              color=colors.HexColor("#e8622a"),
                              spaceAfter=8, spaceBefore=2)

        # ── Construir historia ─────────────────────────────────────────
        buf_pdf = _io.BytesIO()
        doc = SimpleDocTemplate(buf_pdf, pagesize=A4,
                                leftMargin=2.2*cm, rightMargin=2.2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        story = []
        hoy_str = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M")

        # Cabecera
        story.append(Paragraph("Relleno Hidraulico (RH)", S_TITLE))
        story.append(Paragraph("Reporte Geomecanico — Analisis Tecnico-Geotecnico", S_SUB))
        story.append(hr())
        story.append(Paragraph(
            f"Fecha: {hoy_str}     Autor: Bradoc Chambilla", S_NOTE))
        story.append(Spacer(1, 0.5*cm))

        # ── Sección 1: Parámetros del Caserón ─────────────────────────
        story.append(Paragraph("1. Parametros del Caseron", S_H2))
        story.append(hr())
        data1 = [
            ["Parametro", "Valor"],
            ["Longitud L (m)",   f"{L:.1f}"],
            ["Ancho W (m)",      f"{W:.1f}"],
            ["Altura H (m)",     f"{H:.1f}"],
            ["Densidad RH (t/m3)", f"{gRH:.2f}"],
            ["Angulo friccion (deg)", f"{phi:.1f}"],
        ]
        story.append(make_tbl(data1, col_w=[9.5*cm, 6.5*cm]))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(
            f"Configuracion detectada: W = {W:.1f} m | H = {H:.1f} m  →  Caso {caso}", S_BODY))

        # ── Sección 2: Resistencia Requerida ──────────────────────────
        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("2. Resistencia Requerida — UCS_RH (Mitchell)", S_H2))
        story.append(hr())
        data2 = [
            ["Concepto", "Valor"],
            ["Caso geometrico",    f"Caso {caso}"],
            ["Formula aplicada",   formula],
            ["UCS_RH calculado (MPa)", f"{UCS_RH:.4f}"],
            ["Angulo de falla alfa (deg)", f"{alpha:.1f}"],
            ["Cohesion requerida c (MPa)", f"{cohesion:.4f}"],
        ]
        story.append(make_tbl(data2, col_w=[9.5*cm, 6.5*cm]))
        story.append(Spacer(1, 0.25*cm))
        data3 = [
            ["Concepto", "Valor"],
            ["Angulo friccion phi (deg)", f"{phi:.1f}"],
            ["Angulo falla alfa (deg)",   f"{alpha:.1f}"],
            ["Densidad RH (t/m3)",       f"{gRH:.2f}"],
            ["Altura caseron H (m)",     f"{H:.1f}"],
            ["Peso cuna Wn (t)",         f"{Wn:.1f}"],
        ]
        story.append(make_tbl(data3, col_w=[9.5*cm, 6.5*cm]))

        # ── Sección 3: Verificación UCS ───────────────────────────────
        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("3. Verificacion contra UCS Ensayado (28 dias)", S_H2))
        story.append(hr())
        data4 = [
            ["Metrica", "Valor"],
            ["UCS requerido (MPa)",     f"{UCS_RH:.3f}"],
            ["UCS maximo 28d (MPa)",    f"{ucs_max:.3f}"],
            ["UCS promedio 28d (MPa)",  f"{ucs_mean:.3f}"],
            ["Factor UCS_ens / UCS_req",
             f"{factor:.2f}  |  {'CUMPLE' if factor >= 1.0 else 'NO CUMPLE'}"],
        ]
        story.append(make_tbl(data4, col_w=[9.5*cm, 6.5*cm]))

        # Tabla detallada por espécimen
        story.append(Spacer(1, 0.25*cm))
        story.append(Paragraph("Detalle por especimen:", S_BODY))
        ucs_local = st.session_state.ucs_df.copy()
        header_u = [["Especimen", "Dia 7 (MPa)", "Dia 14 (MPa)", "Dia 28 (MPa)", "Cumple?"]]
        rows_u = [
            [r["Especimen"], f"{r['Dia7_MPa']:.3f}", f"{r['Dia14_MPa']:.3f}",
             f"{r['Dia28_MPa']:.3f}",
             "SI" if r["Dia28_MPa"] >= UCS_RH else "NO"]
            for _, r in ucs_local.iterrows()
        ]
        story.append(make_tbl(
            header_u + rows_u,
            col_w=[4.5*cm, 3*cm, 3*cm, 3.2*cm, 2.3*cm]
        ))

        # ── Sección 4: Gráficos ────────────────────────────────────────
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("4. Graficos Geomecanicos", S_H2))
        story.append(hr())

        try:
            story.append(Paragraph(
                "4.1  Distribucion de Presion Vertical en el Relleno", S_BODY))
            story.append(Spacer(1, 0.2*cm))
            story.append(fig_to_rli(fig_g1, w_cm=15.5, h_cm=8.5))
            story.append(Spacer(1, 0.6*cm))
            story.append(Paragraph(
                "4.2  Comparativa UCS a 28 dias vs Requerimiento Geomecanico", S_BODY))
            story.append(Spacer(1, 0.2*cm))
            story.append(fig_to_rli(fig_g2, w_cm=15.5, h_cm=8.5))
        except Exception as e_img:
            story.append(Paragraph(
                f"Nota: graficos no disponibles ({e_img}). "
                "Instale kaleido con: pip install kaleido", S_NOTE))

        # Pie
        story.append(Spacer(1, 0.6*cm))
        story.append(hr())
        story.append(Paragraph(
            f"Sistema RH v1.0  |  Generado: {hoy_str}  |  Bradoc Chambilla",
            S_RIGHT))

        doc.build(story)
        buf_pdf.seek(0)

        fname = f"Reporte_Geomecanico_RH_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        st.download_button(
            label="⬇️ Descargar Reporte PDF",
            data=buf_pdf,
            file_name=fname,
            mime="application/pdf",
            use_container_width=True,
        )
        st.success(f"✔ Reporte generado: {fname}  — haga clic arriba para descargar.")


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
hoy = datetime.datetime.now().strftime("%d/%m/%Y")
st.markdown(f"""
<style>
.footer-box {{
    margin-top: 40px; padding: 18px 24px; width: 100%; text-align: center;
    background: #fff3e6; border-top: 3px solid #e8622a;
    border-radius: 10px; font-size: 13px; color: #6b2d00;
}}
.footer-title {{ font-family: 'DM Serif Display', serif; font-size: 16px; color: #8b3a00; font-weight: 700; }}
</style>
<div class="footer-box">
    <div class="footer-title">💧 Relleno Hidráulico · Sistema RH</div>
    <div>Análisis técnico-geomecánico y diseño de relleno hidráulico</div>
    <br>
    <div>Versión 1.0 · Actualizado el {hoy} · Desarrollado por: <b>Bradoc Chambilla</b></div>
</div>
""", unsafe_allow_html=True)
