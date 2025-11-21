import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Fintech Simulator", layout="wide", page_icon="💎")

# --- LE DESIGN HACK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
        color: #FFFFFF;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #262730;
        color: white;
        border-radius: 10px;
        border: 1px solid #41444C;
    }

    div[data-testid="metric-container"] {
        background-color: #1C1E26;
        border: 1px solid #2E303E;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        border-color: #00D4FF;
    }

    div[data-testid="metric-container"] label {
        color: #A0AAB8;
        font-size: 0.9rem;
    }

    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #FFFFFF;
    }

    h1 {
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00D4FF, #005bea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_text = st.columns([1, 10])
with col_text:
    st.title("Wealth Simulator")
    st.caption("Design inspiré des néobanques")

st.write("")

# --- ONGLETS ---
tab1, tab2 = st.tabs(["💎 ÉPARGNE & INTÉRÊTS", "🏠 IMMOBILIER"])

# ==============================================================================
# ONGLET 1 : ÉPARGNE
# ==============================================================================
with tab1:
    col_in1, col_in2, col_in3, col_in4 = st.columns(4)

    with col_in1:
        capital = st.number_input("Capital initial (€)", value=1000, step=100, format="%d")
    with col_in2:
        mensuel = st.number_input("Ajout mensuel (€)", value=200, step=50, format="%d")
    with col_in3:
        taux = st.number_input("Rendement (%)", value=5.0, step=0.1, format="%.1f")
    with col_in4:
        duree = st.slider("Durée (années)", 1, 40, 15)

    st.divider()

    # --- CALCULS ---
    data = []
    taux_mensuel = (taux / 100) / 12

    for annee in range(duree + 1):
        mois = annee * 12
        versement_total = capital + (mensuel * mois)

        if taux > 0:
            val_capital = capital * (1 + taux_mensuel) ** mois
            val_mensuel = mensuel * (((1 + taux_mensuel) ** mois - 1) / taux_mensuel)
            total = val_capital + val_mensuel
        else:
            total = versement_total

        interets = total - versement_total
        data.append({"Année": annee, "Capital Investi": versement_total, "Intérêts Composés": interets})

    df = pd.DataFrame(data)

    total_final = df.iloc[-1]["Capital Investi"] + df.iloc[-1]["Intérêts Composés"]
    gain_total = df.iloc[-1]["Intérêts Composés"]

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Patrimoine Final", f"{total_final:,.0f} €".replace(",", " "))
    kpi2.metric("Total Investi", f"{df.iloc[-1]['Capital Investi']:,.0f} €".replace(",", " "))
    kpi3.metric("Gains (Intérêts)", f"+ {gain_total:,.0f} €".replace(",", " "), delta="Passif")

    # --- GRAPHIQUE ---
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Année"], y=df["Capital Investi"],
        mode='lines', name='Capital Investi',
        stackgroup='one', line=dict(width=0),
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))

    fig.add_trace(go.Scatter(
        x=df["Année"], y=df["Intérêts Composés"] + df["Capital Investi"],
        mode='lines', name='Total avec Intérêts',
        stackgroup='one', line=dict(width=2, color='#00D4FF'),
        fillcolor='rgba(0, 91, 234, 0.6)'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="white"),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, showline=True, linecolor="#41444C"),
        yaxis=dict(showgrid=True, gridcolor="#262730")
    )

    st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# ONGLET 2 : IMMOBILIER
# ==============================================================================
with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        immo_montant = st.number_input("Montant du prêt (€)", value=250000, step=5000, format="%d")
    with c2:
        immo_taux = st.number_input("Taux crédit (%)", value=3.9, step=0.1, format="%.1f")
    with c3:
        immo_duree = st.slider("Durée (ans)", 7, 30, 25)

    st.divider()

    # Calculs
    mois_total = immo_duree * 12
    tm = (immo_taux / 100) / 12
    if immo_taux > 0:
        mensualite = immo_montant * (tm * (1 + tm) ** mois_total) / ((1 + tm) ** mois_total - 1)
    else:
        mensualite = immo_montant / mois_total

    interet_total_estime = (mensualite * mois_total) - immo_montant

    k1, k2, k3 = st.columns(3)
    k1.metric("Mensualité", f"{mensualite:,.2f} €")
    k2.metric("Coût total crédit", f"{interet_total_estime:,.2f} €", delta="- Intérêts banque", delta_color="inverse")
    k3.metric("Total payé", f"{(immo_montant + interet_total_estime):,.2f} €")

    # Donut
    labels = ['Capital (La maison)', 'Intérêts (La banque)']
    values = [immo_montant, interet_total_estime]
    colors = ['#00D4FF', '#FF0055']

    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig_pie.update_traces(hoverinfo='label+value', textinfo='percent', marker=dict(colors=colors))

    fig_pie.update_layout(
        title_text="Répartition du coût total",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="white"),
        showlegend=True
    )

    st.plotly_chart(fig_pie, use_container_width=True)