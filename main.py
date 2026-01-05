import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Share Illusion Simulator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a stunning UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #60A5FA 100%);
        font-family: 'Poppins', sans-serif;
        color: white;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
    }
    
    h1, h2, h3 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(16,185,129,0.5);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .metric-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        animation: pulse 4s infinite;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
    st.header("🛠️ Input Parameters")
    
    A = st.number_input("No of Shareholders", value=1000, min_value=1, step=1)
    C = st.number_input("Production (Units)", value=2000, min_value=1, step=1)
    D = st.number_input("Selling Price per Unit", value=6000.0, min_value=0.0, step=100.0)
    E = st.number_input("Shares per Shareholder", value=2000, min_value=1, step=1)
    F = st.number_input("Production Cost per Unit", value=250.0, min_value=0.0, step=10.0)
    G = st.number_input("Operating Cost per Unit", value=1238.72180451128, min_value=0.0, step=10.0)
    M = st.number_input("Corporate Tax Rate", value=0.30, min_value=0.0, max_value=1.0, step=0.05)
    P = st.number_input("Dividend Tax Rate", value=0.05, min_value=0.0, max_value=1.0, step=0.01)
    
    compute = st.button("🔮 Compute Illusion")

# Main app
st.title("💫 Share Illusion Simulator")
st.markdown("Explore the fascinating economic balance between shareholders and external people in this interactive model.")

if compute:
    # Core calculations
    B = C - A                          # External People
    if B < 0:
        st.error("Production must be greater than or equal to No of Shareholders.")
        st.stop()
    H = C * F                          # Production Cost
    I = C * G                          # Operating Cost
    J = H + I                          # Total Cost
    K = C * D                          # Revenue
    L = K - J                          # Gross Profit
    N = L * M                          # Corporate Tax
    O = L - N                          # Profit after Tax
    Q = O * P                          # Dividend Tax
    R = O - Q                          # Dividend after Tax
    S = A * E                          # Total Shares
    T = R / S if S else 0              # Dividend Per Share
    U = R / A if A else 0              # Dividend Per Shareholder
    V = N + Q                          # Total Tax to Government
    W = V                              # Government Expenditure
    X = J                              # Company Expenditure
    Y = W + X                          # Total Expenditure
    Z = Y / B if B else 0              # Expenditure Per External Person

    # DataFrame for detailed view
    data = {
        "Field Name": [
            "No of Shareholders", "No of External People", "Production", "Selling Price",
            "Shares per Shareholder", "Production Cost Per Unit", "Operating Cost Per Unit",
            "Production Cost", "Operating Cost", "Total Cost", "Revenue", "Gross Profit",
            "Corporate Tax Rate", "Corporate Tax", "Profit after Tax", "Dividend Tax Rate",
            "Dividend Tax", "Dividend after Tax", "Total Shares", "Dividend Per Share",
            "Dividend Per Shareholder", "Tax to Government", "Govt Expenditure",
            "Company Expenditure", "Total Expenditure", "Expenditure Per External"
        ],
        "Value": [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z],
        "Code": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    }
    df = pd.DataFrame(data)

    # Key metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>Dividend Per Shareholder</h3><h1>${U:,.2f}</h1></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>Expenditure Per External</h3><h1>${Z:,.2f}</h1></div>", unsafe_allow_html=True)
    with col3:
        balance = "Perfectly Balanced ✨" if abs(U - Z) < 1 else f"Unbalanced (Diff: ${abs(U - Z):,.2f})"
        st.markdown(f"<div class='metric-card'><h3>Illusion Status</h3><h1>{balance}</h1></div>", unsafe_allow_html=True)

    # Detailed table
    with st.expander("📊 Detailed Calculations", expanded=True):
        st.dataframe(df.style.format({"Value": "{:,.4f}"}), use_container_width=True)

    # Visualizations
    st.header("📈 Visual Insights")

    # 1. Pie chart - Breakdown of profit usage
    pie_data = pd.DataFrame({
        "Category": ["Production Cost", "Operating Cost", "Corporate Tax", "Dividend Tax", "Dividend to Shareholders"],
        "Amount": [H, I, N, Q, R]
    })
    fig_pie = px.pie(pie_data, values="Amount", names="Category", title="Where the Money Goes",
                     color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.4)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig_pie, use_container_width=True)

    # 2. Bar chart - Key financials
    bar_data = pd.DataFrame({
        "Metric": ["Revenue", "Total Cost", "Gross Profit", "Profit after Tax", "Dividend after Tax"],
        "Value": [K, J, L, O, R]
    })
    fig_bar = px.bar(bar_data, x="Metric", y="Value", title="Financial Overview",
                     color="Metric", color_discrete_sequence=px.colors.sequential.Teal)
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    # 3. Comparison: Shareholders vs Externals
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dual.add_trace(go.Bar(name="Total Received", x=["Shareholders", "Externals"], y=[U * A, Z * B],
                              marker_color="#60A5FA"), secondary_y=False)
    fig_dual.add_trace(go.Scatter(name="Per Person", x=["Shareholders", "Externals"], y=[U, Z],
                                  mode="lines+markers+text", text=[f"${U:,.0f}", f"${Z:,.0f}"],
                                  textposition="top center", line=dict(color="#10B981", width=4)), secondary_y=True)
    fig_dual.update_layout(title="Shareholders vs External People - The Illusion",
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig_dual.update_yaxes(title_text="Total Amount ($)", secondary_y=False)
    fig_dual.update_yaxes(title_text="Per Person ($)", secondary_y=True)
    st.plotly_chart(fig_dual, use_container_width=True)

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.8); margin-top:50px;'>Built with ❤️ using Streamlit & Plotly | xAI Grok</p>", unsafe_allow_html=True)