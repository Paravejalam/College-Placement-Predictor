import numpy as np
import streamlit as st
from ml.preprocess import prepare_input


def what_if_simulator(model, base_inputs: dict, current_prob: float):
    """
    Read-only What-If Simulator
    - Does NOT touch session state
    - Does NOT reset prediction
    - Uses same ML pipeline as real prediction
    """

    st.markdown("## 🔮 What-If Simulator")
    st.caption("Simulate skill improvements without changing your actual profile")

    # -------------------------------------------------
    # READ-ONLY BASE INPUTS (from prediction snapshot)
    # -------------------------------------------------
    simulated = base_inputs.copy()

    col1, col2 = st.columns(2)

    with col1:
        simulated["aptitude"] = st.slider(
            "Aptitude Score",
            0, 10,
            int(base_inputs["aptitude"]),
            key="whatif_aptitude"
        )

        simulated["technical"] = st.slider(
            "Technical Score",
            0, 10,
            int(base_inputs["technical"]),
            key="whatif_technical"
        )

    with col2:
        simulated["communication"] = st.slider(
            "Communication Score",
            0, 10,
            int(base_inputs["communication"]),
            key="whatif_communication"
        )

        simulated["overall"] = st.slider(
            "Overall Skills",
            0, 10,
            int(base_inputs.get("overall_skills", 0)),
            key="whatif_overall"
        )

    st.divider()

    # -------------------------------------------------
    # SIMULATE (NO STATE MUTATION)
    # -------------------------------------------------
    if st.button("🔍 Simulate Impact", use_container_width=True):

        # 🔁 MAP TO MODEL FEATURE SCHEMA (CRITICAL FIX)
        simulated_model_inputs = {
            "cgpa": simulated["cgpa"],
            "internships": simulated["internships"],
            "projects": simulated["projects"],
            "certifications": simulated["certifications"],
            "aptitude_score": simulated["aptitude"],
            "technical_score": simulated["technical"],
            "communication_score": simulated["communication"],
            "overall_skills": simulated["overall"],
            "domain": simulated["domain"],  # encoded inside prepare_input
        }

        model_input = np.array(
            prepare_input(simulated_model_inputs),
            dtype=float
        ).reshape(1, -1)

        new_prob = model.predict_proba(model_input)[0][1] * 100
        delta = new_prob - current_prob

        # -------------------------------------------------
        # OUTPUT
        # -------------------------------------------------
        st.markdown("### 📊 Simulated Placement Probability")
        st.metric(
            label="Placement Probability",
            value=f"{new_prob:.2f}%",
            delta=f"{delta:+.2f}%"
        )

        if new_prob < 50:
            st.error(f"🔴 Placement Risk Detected ({new_prob:.2f}%)")
        else:
            st.success(f"🟢 Strong Placement Chance ({new_prob:.2f}%)")
