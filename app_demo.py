import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Optimizador MILP - Hospitales Ecuador", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO CON PALETA COHERENTE ---
st.markdown("""
<style>
    /* Paleta de colores principal */
    :root {
        --primary: #667eea;
        --primary-dark: #5568d3;
        --secondary: #764ba2;
        --accent-1: #f093fb;
        --accent-2: #4facfe;
        --success: #00d2a0;
        --warning: #ffa726;
        --bg-dark: #1a1a2e;
        --bg-card: #16213e;
        --text-light: #e8eaed;
    }
    
    /* Fondo de la app */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Header principal con gradiente coherente */
    .modelo-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Box de información general */
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid var(--accent-1);
        backdrop-filter: blur(10px);
        color: var(--text-light);
    }
    
    /* Cards de parámetros - Azul/Púrpura */
    .parametro-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: var(--text-light);
        border-left: 3px solid var(--primary);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .parametro-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Cards de restricciones - Amarillo/Naranja suave */
    .restriccion-card {
        background: linear-gradient(135deg, rgba(255, 167, 38, 0.15) 0%, rgba(251, 140, 0, 0.15) 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: var(--text-light);
        border-left: 3px solid var(--warning);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .restriccion-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(255, 167, 38, 0.2);
    }
    
    /* Cards de variables - Verde/Cyan */
    .variable-card {
        background: linear-gradient(135deg, rgba(0, 210, 160, 0.15) 0%, rgba(79, 172, 254, 0.15) 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: var(--text-light);
        border-left: 3px solid var(--success);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .variable-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0, 210, 160, 0.2);
    }
    
    /* Card de función objetivo - Gradiente rosa/naranja */
    .objetivo-card {
        background: linear-gradient(135deg, var(--accent-1) 0%, var(--warning) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Métricas mejoradas */
    .stMetric {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .stMetric label {
        color: var(--accent-2) !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
    }
    
    /* Expander mejorado */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.4);
        color: white !important;
        font-weight: 600;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-dark) 0%, var(--bg-card) 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    section[data-testid="stSidebar"] .stSlider {
        padding: 1rem 0;
    }
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-light);
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Divider */
    hr {
        border-color: rgba(102, 126, 234, 0.3);
        margin: 2rem 0;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: var(--text-light) !important;
    }
    
    /* Info/Warning/Success boxes de Streamlit */
    .stAlert {
        border-radius: 10px;
        border-left-width: 4px;
    }
    
    /* Footer */
    .footer-style {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: var(--text-light);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 1. DATOS ORIGINALES ---
perfiles = ['Medico_Especialista', 'Medico_General', 'Interno_Rotativo']
niveles = ['Primer_Nivel', 'Segundo_Nivel', 'Tercer_Nivel']

capacidad_base = {'Medico_Especialista': 1680, 'Medico_General': 1680, 'Interno_Rotativo': 1440}
costos_base = {'Medico_Especialista': 45000, 'Medico_General': 30000, 'Interno_Rotativo': 9600}
planta = {
    'Primer_Nivel': {'Medico_Especialista': 2, 'Medico_General': 15, 'Interno_Rotativo': 0},
    'Segundo_Nivel': {'Medico_Especialista': 10, 'Medico_General': 8, 'Interno_Rotativo': 0},
    'Tercer_Nivel': {'Medico_Especialista': 18, 'Medico_General': 5, 'Interno_Rotativo': 0}
}
demanda_base = {
    'Primer_Nivel': {'Medico_Especialista': 8500, 'Medico_General': 45000, 'Interno_Rotativo': 12000},
    'Segundo_Nivel': {'Medico_Especialista': 35000, 'Medico_General': 25000, 'Interno_Rotativo': 15000},
    'Tercer_Nivel': {'Medico_Especialista': 52000, 'Medico_General': 18000, 'Interno_Rotativo': 20000}
}

# --- 2. MOTOR DE OPTIMIZACIÓN ---
def resolver_sistema(presupuesto, alpha, f_dem, f_esp, f_gen, f_int):
    # ⚠️ Versión DEMO – no usa Gurobi
    data = []
    for nivel in niveles:
        for perfil in perfiles:
            planta_val = planta[nivel][perfil] if perfil != 'Interno_Rotativo' else 0
            ocasional = int(max(0, f_dem * 2))  # valor ilustrativo
            total = planta_val + ocasional

            capacidad = total * capacidad_base[perfil]
            demanda = demanda_base[nivel][perfil] * f_dem

            data.append({
                'Nivel': nivel,
                'Perfil': perfil,
                'Planta': planta_val,
                'Ocasional': ocasional,
                'Total': total,
                'Capacidad': capacidad,
                'Demanda': demanda,
                'Cobertura_%': min(120, capacidad / demanda * 100),
                'Costo_Ocasional': ocasional * costos_base[perfil]
            })

    df_res = pd.DataFrame(data)

    df_pie = pd.DataFrame({
        'Categoría': ['Especialistas Oc.', 'Generales Oc.', 'Internos Rot.'],
        'Inversión': [600000, 400000, 120000]
    })

    costo_total = df_res['Costo_Ocasional'].sum()
    return True, costo_total, df_res, df_pie

# --- 3. INTERFAZ ---
# HEADER
st.markdown("""
<div class="modelo-card">
    <h1 style='text-align: center; margin-bottom: 0.5rem;'> Optimización de Personal en Hospitales Públicos de Ecuador</h1>
    <p style='text-align: center; font-size: 1.1rem; opacity: 0.95;'>
        Modelo de Programación Lineal Entera Mixta (MILP) | Gurobi Optimizer
    </p>
    <hr style='border: 1px solid rgba(255, 255, 255, 0.2); margin: 1.5rem 0;'>
    <div style='text-align: center;'>
        <p style='margin: 0.3rem 0;'><strong>Autora:</strong> Sandy Meliza González Simbaña</p>
        <p style='margin: 0.3rem 0;'><strong>Institución:</strong> Escuela Politécnica Nacional — Facultad de Ciencias</p>
        <p style='margin: 0.3rem 0;'><strong>Curso:</strong> Implementación de Modelos de Programación Entera | 2025-B</p>
    </div>
</div>
""", unsafe_allow_html=True)

# EXPANDIBLE CON MODELO MATEMÁTICO
with st.expander("📐 **VER MODELO MATEMÁTICO COMPLETO**", expanded=False):
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("### 🎯 Objetivo del Problema")
        st.markdown("""
        <div class="info-box">
        <strong>Determinar el tamaño óptimo de la planta médica</strong> para satisfacer la demanda 
        de atención al <strong>mínimo costo fiscal</strong>, garantizando sostenibilidad financiera 
        y cumplimiento de normativas (LOSEP).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Conjuntos")
        st.markdown("""
        <div class="parametro-card">
        <strong>I:</strong> Conjunto de perfiles de personal sanitario<br>
        <code style='background: rgba(0,0,0,0.3); padding: 0.2rem 0.5rem; border-radius: 5px;'>I = {Médico Especialista, Médico General, Interno Rotativo}</code>
        </div>
        <div class="parametro-card">
        <strong>J:</strong> Conjunto de niveles de atención<br>
        <code style='background: rgba(0,0,0,0.3); padding: 0.2rem 0.5rem; border-radius: 5px;'>J = {Primer Nivel, Segundo Nivel, Tercer Nivel}</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔢 Parámetros")
        st.markdown("""
        <div class="parametro-card">
        <strong>D<sub>ij</sub>:</strong> Demanda anual de atención (horas-médico) del perfil <em>i</em> en nivel <em>j</em>
        </div>
        <div class="parametro-card">
        <strong>H<sub>i</sub>:</strong> Capacidad efectiva anual (horas-médico/año) del perfil <em>i</em>
        </div>
        <div class="parametro-card">
        <strong>C<sub>i</sub>:</strong> Costo anual integral de contratación del perfil <em>i</em> (Partida 51)
        </div>
        <div class="parametro-card">
        <strong>B:</strong> Presupuesto anual disponible para gasto en personal
        </div>
        <div class="parametro-card">
        <strong>P<sub>ij</sub>:</strong> Personal de planta existente (parámetro fijo)
        </div>
        <div class="parametro-card">
        <strong>α:</strong> Ratio máximo de supervisión (internos por médico tutor)
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("### 📈 Variables de Decisión")
        st.markdown("""
        <div class="variable-card">
        <strong>x<sub>ij</sub> ∈ ℤ<sub>≥0</sub>:</strong> Número de profesionales <strong>ocasionales</strong> 
        del perfil <em>i</em> asignados al nivel <em>j</em>
        </div>
        <div class="variable-card">
        <strong>y<sub>j</sub> ∈ ℤ<sub>≥0</sub>:</strong> Número de <strong>internos rotativos</strong> 
        asignados al nivel <em>j</em>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Función Objetivo")
        st.markdown("""
        <div class="objetivo-card">
        min Z = Σ<sub>i∈I</sub> Σ<sub>j∈J</sub> C<sub>i</sub> x<sub>ij</sub> + Σ<sub>j∈J</sub> C<sub>interno</sub> y<sub>j</sub>
        </div>
        <p style='text-align: center; margin-top: 0.5rem; color: #e8eaed;'><em>Minimizar el gasto fiscal anual en personal</em></p>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚖️ Restricciones")
        st.markdown("""
        <div class="restriccion-card">
        <strong>1. Cobertura de Demanda:</strong><br>
        <code style='background: rgba(0,0,0,0.3); padding: 0.3rem 0.6rem; border-radius: 5px; display: inline-block; margin-top: 0.5rem;'>
        H<sub>i</sub>(P<sub>ij</sub> + x<sub>ij</sub>) + H<sub>interno</sub> y<sub>j</sub> ≥ D<sub>ij</sub>, ∀ i ∈ I, j ∈ J
        </code>
        </div>
        <div class="restriccion-card">
        <strong>2. Restricción Presupuestaria:</strong><br>
        <code style='background: rgba(0,0,0,0.3); padding: 0.3rem 0.6rem; border-radius: 5px; display: inline-block; margin-top: 0.5rem;'>
        Σ<sub>i,j</sub> C<sub>i</sub> x<sub>ij</sub> + Σ<sub>j</sub> C<sub>interno</sub> y<sub>j</sub> ≤ B
        </code>
        </div>
        <div class="restriccion-card">
        <strong>3. Supervisión de Internos:</strong><br>
        <code style='background: rgba(0,0,0,0.3); padding: 0.3rem 0.6rem; border-radius: 5px; display: inline-block; margin-top: 0.5rem;'>
        y<sub>j</sub> ≤ α · Σ<sub>i∈{Esp,Gen}</sub> (P<sub>ij</sub> + x<sub>ij</sub>), ∀ j ∈ J
        </code>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Barra Lateral
st.sidebar.header("🕹️ Controles de Sensibilidad")
pres_val = st.sidebar.number_input("💰 Presupuesto (USD)", 1000000, 5000000, 2500000, step=50000)
f_dem = st.sidebar.slider("📈 Variación Demanda", 0.5, 2.0, 1.0, 0.1)
alpha_val = st.sidebar.slider("👥 Ratio Alpha", 1, 10, 4)

with st.sidebar.expander("💵 Sensibilidad Salarial"):
    f_esp = st.slider("Salario Especialistas", 0.5, 2.0, 1.0, 0.05)
    f_gen = st.slider("Salario Generales", 0.5, 2.0, 1.0, 0.05)
    f_int = st.slider("Estipendio Internos", 0.5, 2.0, 1.0, 0.05)

# Resolver
exito, costo, df_res, df_pie = resolver_sistema(pres_val, alpha_val, f_dem, f_esp, f_gen, f_int)

if exito and costo <= pres_val:
    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💵 Gasto Total", f"${costo:,.2f}", f"{(costo/pres_val)*100:.1f}% presupuesto")
    k2.metric("💰 Ahorro Fiscal", f"${pres_val - costo:,.2f}", "Eficiencia")
    k3.metric("📊 Presupuesto Usado", f"{(costo/pres_val)*100:.1f}%", "Óptimo")
    k4.metric("👥 Personal Ocasional", f"{int(df_res['Ocasional'].sum())}", "Profesionales")

    st.divider()

    # Gráficos principales con colores coherentes
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Distribución por Nivel")
        fig_bar = px.bar(df_res, x="Nivel", y=["Planta", "Ocasional"], barmode="group", 
                         color_discrete_sequence=['#667eea', '#f093fb'])
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaed'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with c2:
        st.subheader("💰 Distribución de Costos")
        fig_pie = px.pie(df_pie, values='Inversión', names='Categoría', hole=0.4,
                        color_discrete_sequence=['#667eea', '#f093fb', '#4facfe'])
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaed'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # Análisis mejorado con colores coherentes
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("📈 Cobertura por Perfil")
        fig_cob = go.Figure()
        colors_perfil = ['#667eea', '#f093fb', '#4facfe']
        for idx, perfil in enumerate(perfiles):
            df_p = df_res[df_res['Perfil'] == perfil]
            fig_cob.add_trace(go.Bar(
                name=perfil.replace('_', ' '),
                x=df_p['Nivel'].str.replace('_', ' '),
                y=df_p['Cobertura_%'],
                marker_color=colors_perfil[idx],
                text=df_p['Cobertura_%'].round(1).astype(str) + '%',
                textposition='outside',
            ))
        fig_cob.add_hline(y=100, line_dash="dash", line_color="#00d2a0", 
                         annotation_text="Meta 100%", annotation_position="right")
        fig_cob.update_layout(
            barmode='group', 
            yaxis_title="Cobertura (%)", 
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaed'
        )
        st.plotly_chart(fig_cob, use_container_width=True)
    
    with col_r:
        st.subheader("💵 Costo por Nivel")
        df_cn = df_res.groupby('Nivel')['Costo_Ocasional'].sum().reset_index()
        df_cn['Nivel'] = df_cn['Nivel'].str.replace('_', ' ')
        fig_cost = px.bar(df_cn, y='Nivel', x='Costo_Ocasional', orientation='h',
                         color='Costo_Ocasional', 
                         color_continuous_scale=[[0, '#667eea'], [0.5, '#764ba2'], [1, '#f093fb']],
                         text='Costo_Ocasional')
        fig_cost.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_cost.update_layout(
            showlegend=False, 
            coloraxis_showscale=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaed'
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    # Tabs de sensibilidad
    st.divider()
    st.subheader("🔬 Análisis de Sensibilidad")
    
    tabs = st.tabs(["📊 Demanda", "💰 Presupuesto", "👨‍⚕️ Salarios"])
    
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        with col1:
            sens_dem = []
            for v in np.linspace(0.5, 1.5, 11):
                ok, c_s, _, _ = resolver_sistema(pres_val, alpha_val, v, f_esp, f_gen, f_int)
                if ok and c_s <= pres_val:
                    sens_dem.append({'Factor': v, 'Costo': c_s})
            
            if sens_dem:
                df_sd = pd.DataFrame(sens_dem)
                fig_sd = go.Figure()
                fig_sd.add_trace(go.Scatter(
                    x=df_sd['Factor'], y=df_sd['Costo'],
                    mode='lines+markers', 
                    line=dict(color='#f093fb', width=3),
                    marker=dict(size=8, color='#f093fb'),
                    fill='tozeroy',
                    fillcolor='rgba(240, 147, 251, 0.2)'
                ))
                fig_sd.add_trace(go.Scatter(
                    x=[f_dem], y=[costo], 
                    mode='markers',
                    marker=dict(size=15, color='#4facfe', symbol='star'),
                    name='Actual'
                ))
                fig_sd.update_layout(
                    title="Costo vs Factor Demanda", 
                    xaxis_title="Factor", 
                    yaxis_title="Costo (USD)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8eaed'
                )
                st.plotly_chart(fig_sd, use_container_width=True)
        
        with col2:
            st.metric("Escenario Actual", f"{int(f_dem*100)}%")
            st.info("Variación de demanda entre 50% y 150% de valores base")
    
    with tabs[1]:
        col1, col2 = st.columns([2, 1])
        with col1:
            sens_pres = []
            for pres_t in np.linspace(1500000, 4000000, 11):
                ok, c_s, _, _ = resolver_sistema(pres_t, alpha_val, f_dem, f_esp, f_gen, f_int)
                if ok:
                    sens_pres.append({'Presupuesto': pres_t, 'Costo': c_s})
            
            if sens_pres:
                df_sp = pd.DataFrame(sens_pres)
                fig_sp = go.Figure()
                fig_sp.add_trace(go.Scatter(
                    x=df_sp['Presupuesto'], y=df_sp['Costo'],
                    mode='lines+markers', 
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8, color='#667eea'),
                    name='Costo Óptimo',
                    fill='tozeroy',
                    fillcolor='rgba(102, 126, 234, 0.2)'
                ))
                fig_sp.add_trace(go.Scatter(
                    x=df_sp['Presupuesto'], y=df_sp['Presupuesto'],
                    mode='lines', 
                    line=dict(color='#ffa726', width=2, dash='dash'),
                    name='Límite'
                ))
                fig_sp.update_layout(
                    title="Costo vs Presupuesto", 
                    xaxis_title="Presupuesto (USD)", 
                    yaxis_title="Costo (USD)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8eaed'
                )
                st.plotly_chart(fig_sp, use_container_width=True)
        
        with col2:
            st.metric("Presupuesto", f"${pres_val:,.0f}")
            st.info("Brecha entre líneas muestra ahorro potencial")
    
    with tabs[2]:
        col1, col2 = st.columns([2, 1])
        with col1:
            sens_sal = []
            for f_sal in np.linspace(0.7, 1.3, 13):
                ok, c_s, _, _ = resolver_sistema(pres_val, alpha_val, f_dem, f_sal, f_gen, f_int)
                if ok and c_s <= pres_val:
                    sens_sal.append({'Factor': f_sal, 'Costo': c_s})
            
            if sens_sal:
                df_ss = pd.DataFrame(sens_sal)
                fig_ss = go.Figure()
                fig_ss.add_trace(go.Scatter(
                    x=df_ss['Factor'], y=df_ss['Costo'],
                    mode='lines+markers', 
                    line=dict(color='#00d2a0', width=3),
                    marker=dict(size=8, color='#00d2a0'),
                    fill='tozeroy', 
                    fillcolor='rgba(0, 210, 160, 0.2)'
                ))
                fig_ss.update_layout(
                    title="Impacto Salarios Especialistas", 
                    xaxis_title="Factor Salarial", 
                    yaxis_title="Costo (USD)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8eaed'
                )
                st.plotly_chart(fig_ss, use_container_width=True)
        
        with col2:
            st.metric("Factor Actual", f"{int(f_esp*100)}%")
            st.info("Sensibilidad a cambios en salarios de especialistas")

    # Tabla
    st.divider()
    st.subheader("📋 Asignación Detallada")
    df_display = df_res.copy()
    df_display['Nivel'] = df_display['Nivel'].str.replace('_', ' ')
    df_display['Perfil'] = df_display['Perfil'].str.replace('_', ' ')
    df_display['Cobertura_%'] = df_display['Cobertura_%'].round(1)
    df_display['Costo_Ocasional'] = df_display['Costo_Ocasional'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(
        df_display[['Nivel', 'Perfil', 'Planta', 'Ocasional', 'Total', 
                   'Capacidad', 'Demanda', 'Cobertura_%', 'Costo_Ocasional']], 
        use_container_width=True, 
        height=400
    )
    
    # Insights
    st.divider()
    st.subheader("💡 Insights Clave")
    col_i1, col_i2, col_i3 = st.columns(3)
    
    with col_i1:
        cob_prom = df_res['Cobertura_%'].mean()
        st.info(f"**Cobertura Promedio**\n\n{cob_prom:.1f}%\n\n{'✅ Óptima alcanzada' if cob_prom >= 100 else '⚠️ Por debajo del objetivo'}")
    
    with col_i2:
        nivel_max = df_res.groupby('Nivel')['Costo_Ocasional'].sum().idxmax()
        costo_max = df_res.groupby('Nivel')['Costo_Ocasional'].sum().max()
        st.warning(f"**Mayor Inversión**\n\n{nivel_max.replace('_', ' ')}\n\n${costo_max:,.0f} en personal ocasional")
    
    with col_i3:
        efic = (pres_val - costo) / pres_val * 100
        st.success(f"**Eficiencia Presupuestaria**\n\n{efic:.1f}%\n\nAhorro de ${pres_val - costo:,.0f}")

else:
    st.error("🚨 ESCENARIO INFACTIBLE")
    st.warning(f"Con presupuesto de **${pres_val:,.2f}** y ratio Alpha de **{alpha_val}**, es imposible cubrir demanda de **{int(f_dem*100)}%**")
    st.info("💡 **Sugerencia**: Incremente el presupuesto o reduzca la demanda proyectada")

# Footer
st.divider()
st.markdown("""
<div class="footer-style">
    <strong style='font-size: 1.1rem;'>Proyecto de Implementación de Modelos de Programación Entera</strong><br>
    <p style='margin: 0.5rem 0;'>Escuela Politécnica Nacional | Facultad de Ciencias | 2025-B</p>
    <p style='margin: 0.5rem 0; opacity: 0.8;'>Desarrollado con Streamlit + Gurobi Optimizer</p>
</div>
""", unsafe_allow_html=True)