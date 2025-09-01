import streamlit as st
import random

# ----------------------------
# Question bank (starter set)
# ----------------------------
question_bank = {
    "Top (Band 5/6 focus)": [
        {
            "q": "Explain how Le Chatelier’s principle predicts the effect of increasing temperature on the equilibrium yield of ammonia in the Haber process. (6 marks)",
            "criteria": [
                "Identifies exothermic/endothermic nature of the reaction",
                "States correct direction of equilibrium shift",
                "Explains reasoning in terms of particle energy",
                "Links prediction to ammonia yield",
                "Uses correct scientific terminology",
            ]
        },
        {
            "q": "Assess the effectiveness of catalysts in industrial chemical processes, using examples from the syllabus. (6 marks)",
            "criteria": [
                "Defines role of catalyst",
                "Explains effect on activation energy",
                "Provides at least one syllabus example (e.g. Haber process, Contact process)",
                "Discusses economic or environmental benefit",
            ]
        }
    ],
    "Middle (Band 4 security)": [
        {
            "q": "Calculate the concentration of HCl if 25 mL of the solution required 30.0 mL of 0.100 M NaOH to neutralise. (3 marks)",
            "criteria": [
                "Balanced equation: HCl + NaOH → NaCl + H2O",
                "Correct mole calculation for NaOH",
                "Final concentration of HCl with units",
            ]
        },
        {
            "q": "Outline how the pH scale is used to compare acidic and basic solutions. (3 marks)",
            "criteria": [
                "Defines pH scale",
                "Explains relationship between pH and H+/OH- concentration",
                "Compares acidic vs basic solutions",
            ]
        }
    ],
    "Lower (avoid Band 2)": [
        {
            "q": "What is the dependent variable in an experiment investigating the effect of temperature on the rate of reaction? (1 mark)",
            "criteria": [
                "Correctly identifies 'rate of reaction'",
            ]
        },
        {
            "q": "Define an isotope. (1 mark)",
            "criteria": [
                "Atoms of the same element with different numbers of neutrons",
            ]
        }
    ]
}

# ----------------------------
# App layout
# ----------------------------
st.title("🧪 Chem Bot – HSC Exam Practice")
st.write("Get targeted practice questions and feedback for HSC Chemistry.")

level = st.selectbox("Choose your group:", list(question_bank.keys()))

if "current_q" not in st.session_state:
    st.session_state.current_q = None
    st.session_state.criteria = None

if st.button("Get Question"):
    q = random.choice(question_bank[level])
    st.session_state.current_q = q["q"]
    st.session_state.criteria = q["criteria"]

if st.session_state.current_q:
    st.subheader("Question")
    st.write(st.session_state.current_q)

    answer = st.text_area("Type your answer here:")

    if st.button("Submit Answer"):
        st.subheader("Feedback")
        criteria = st.session_state.criteria
        for point in criteria:
            if any(word.lower() in answer.lower() for word in point.lower().split()):
                st.success(f"✅ Covered: {point}")
            else:
                st.warning(f"⚠️ Missing: {point} – add this detail next time.")
