import os
import re
import random
import streamlit as st

# ---------- CONFIG ----------
APP_TITLE = "🧪 Chem Bot — HSC Exam Coach"
INTRO = "Targeted past-paper style questions with marker-style feedback, exemplars, and next steps."

# ---------- QUESTION BANK (starter set; expand freely) ----------
# Each item has: prompt, criteria (marker points), topic, band_target
QUESTION_BANK = [
    # TOP (Band 5/6)
    {
        "group": "Top (Band 5/6)",
        "topic": "Equilibrium / Haber",
        "prompt": "Explain how Le Chatelier’s principle predicts the effect of increasing temperature on the equilibrium yield of ammonia in the Haber process. (6 marks)",
        "criteria": [
            "Identifies exothermic direction of forward reaction for ammonia formation (or correctly states enthalpy change).",
            "States correct direction of equilibrium shift when temperature increases.",
            "Explains particle/energy reasoning (collision energy, endothermic favoured when T ↑).",
            "Links shift to effect on ammonia yield explicitly.",
            "Uses correct scientific terminology and avoids vague everyday language.",
            "Provides a concise concluding statement that answers the question."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "group": "Top (Band 5/6)",
        "topic": "Catalysis",
        "prompt": "Assess the effectiveness of catalysts in industrial chemical processes, using syllabus-relevant examples. (6 marks)",
        "criteria": [
            "Defines catalyst and effect on activation energy (Ea).",
            "Explains increased rate without shifting equilibrium position.",
            "Uses at least one relevant industrial example (e.g., Haber, Contact).",
            "Discusses economic/environmental advantages from catalysis.",
            "Integrates data/conditions where appropriate (temperature/pressure).",
            "Clear judgement/assessment, not just description."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },

    # MIDDLE (Band 4 security)
    {
        "group": "Middle (Band 4 security)",
        "topic": "Acid–Base Titration",
        "prompt": "25.0 mL of HCl is titrated with 0.100 M NaOH. The endpoint occurs at 30.0 mL of NaOH. Calculate the concentration of HCl. (3 marks)",
        "criteria": [
            "Balanced: HCl + NaOH → NaCl + H2O (1:1).",
            "Correct moles of NaOH: n = C × V (in L).",
            "Correct [HCl] with units and appropriate significant figures."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },
    {
        "group": "Middle (Band 4 secu

