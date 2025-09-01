import os
import re
import random
import streamlit as st

# ---------- CONFIG ----------
APP_TITLE = "🧪 Chem Bot — HSC Exam Coach"
INTRO = "Targeted past-paper style questions with marker-style feedback, an exemplar, and step-by-step coaching to build stronger answers."

# ---------- QUESTION BANK (expand freely) ----------
QUESTION_BANK = [
    # TOP (Band 5/6)
    {
        "group": "Top (Band 5/6)",
        "topic": "Equilibrium / Haber",
        "prompt": "Explain how Le Chatelier’s principle predicts the effect of increasing temperature on the equilibrium yield of ammonia in the Haber process. (6 marks)",
        "criteria": [
            "Identifies the forward reaction for ammonia formation as exothermic (or correctly states enthalpy change).",
            "States the correct equilibrium shift when temperature increases.",
            "Explains why: added heat favours the endothermic direction to oppose the change.",
            "Links the shift clearly to the effect on ammonia yield.",
            "Uses correct scientific terminology; avoids vague language.",
            "Finishes with a concise concluding statement that answers the question."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "group": "Top (Band 5/6)",
        "topic": "Catalysis",
        "prompt": "Assess the effectiveness of catalysts in industrial chemical processes, using syllabus-relevant examples. (6 marks)",
        "criteria": [
            "Defines a catalyst and its effect on activation energy (Ea).",
            "Explains why catalysts increase rate without changing equilibrium position.",
            "Uses at least one relevant industrial example (e.g., Haber, Contact).",
            "Discusses economic and/or environmental advantages.",
            "Integrates relevant conditions/data where appropriate.",
            "Provides a clear judgement/assessment, not just description."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },

    # MIDDLE (Band 4 security)
    {
        "group": "Middle (Band 4 security)",
        "topic": "Acid–Base Titration",
        "prompt": "25.0 mL of HCl is titrated with 0.100 M NaOH. The endpoint occurs at 30.0 mL of NaOH. Calculate the concentration of HCl. (3 marks)",
        "criteria": [
            "Balanced equation: HCl + NaOH → NaCl + H2O (1:1).",
            "Correct moles of NaOH: n = C × V (in L).",
            "Correct [HCl] with units and appropriate significant figures."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },
    {
        "group": "Middle (Band 4 security)",
        "topic": "pH Basics",
        "prompt": "Outline how the pH scale is used to compare acidic and basic solutions. (3 marks)",
        "criteria": [
            "Defines pH in terms of hydrogen ion concentration.",
            "Explains that lower pH means higher [H+] (acidic) and higher pH means higher [OH−] (basic).",
            "Mentions ten-fold change in concentration per 1 pH unit or gives a clear comparative statement."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },

    # LOWER (limit Band 2)
    {
        "group": "Lower (limit Band 2)",
        "topic": "Variables",
        "prompt": "In an experiment investigating temperature and rate of reaction, what is the dependent variable? (1 mark)",
        "criteria": [
            "Identifies 'rate of reaction' as the dependent variable."
        ],
        "band_target": "Goal: Lift to Band 3; avoid Band 2."
    },
    {
        "group": "Lower (limit Band 2)",
        "topic": "Isotopes",
        "prompt": "Define an isotope. (1 mark)",
        "criteria": [
            "Atoms of the same element with different numbers of neutrons."
        ],
        "band_target": "Goal: Lift to Band 3; avoid Band 2."
    },
]

GROUPS = ["Top (Band 5/6)", "Middle (Band 4 security)", "Lower (limit Band 2)"]

# ---------- SIMPLE HEURISTICS FOR CALC ITEMS ----------
def approx_equal(a, b, tol=0.01):
    try:
        return abs(float(a) - float(b)) <= tol
    except:
        return False

def titration_expected_conc():
    # 25.0 mL HCl; 30.0 mL of 0.100 M NaOH; 1:1 reaction
    n_naoh = 0.100 * (30.0 / 1000)  # 0.00300 mol
    c_hcl = n_naoh / (25.0 / 1000)  # 0.120 M
    return 0.120

# ---------- LLM FEEDBACK (OpenAI) ----------
def llm_feedback(answer, prompt, criteria, group, topic, band_target):
    """
    If OPENAI_API_KEY is set, uses OpenAI to generate rich, student-friendly feedback.
    Otherwise, falls back to a structured heuristic.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    criteria_text = "\n- " + "\n- ".join(criteria)

    system = f"""
You are an experienced NSW HSC Chemistry marker.
Tone: warm, specific, encouraging, and student-friendly.
Always return sections with these EXACT headings in this order:
1) ✅ Strengths
2) ⚠️ Marks Lost (mapped to criteria)
3) 🧱 Build It Up (step-by-step coaching using simple language in this sequence: identify → describe → explain → conclude; do not use any rubric jargon)
4) 🧠 Exemplar Response
5) 🔧 Next Steps (3 bullet points)
6) ☑️ Final Checklist

Target group: {group}. Topic: {topic}. {band_target}
Focus on units/sig figs and explicit links back to the question where relevant.
Keep it concise but not superficial; make it feel like feedback from a real teacher.
"""

    user = f"""
QUESTION:
{prompt}

CRITERIA:
{criteria_text}

STUDENT ANSWER:
{answer}
"""

    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI()  # reads key from env var
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=0.2
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ LLM error: {e}\n\n" + heuristic_feedback(answer, prompt, criteria, group, topic, band_target)
    else:
        return heuristic_feedback(answer,_
