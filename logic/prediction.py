import plotly.graph_objects as go
import streamlit as st


def predict_probability(model, X):
    return round(model.predict_proba(X)[0][1] * 100, 2)

def render_gauge(prob):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob,
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#4f8cff"},
            "steps": [
                {"range": [0, 40], "color": "#ff4d4d"},
                {"range": [40, 70], "color": "#ffa500"},
                {"range": [70, 100], "color": "#4caf50"},
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
