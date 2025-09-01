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
        "group": "Middle (Band 4 security)",
        "topic": "pH Basics",
        "prompt": "Outline how the pH scale is used to compare acidic and basic solutions. (3 marks)",
        "criteria": [
            "Defines pH in terms of hydrogen ion concentration.",
            "Explains low pH = acidic (higher [H+]); high pH = basic (higher [OH-]).",
            "Links one unit pH change to tenfold change in [H+]/[OH-] or gives clear comparative statement."
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

# ---------- SIMPLE HEURISTICS FOR CALC QUESTIONS ----------
def check_sig_figs(value_str):
    # crude significant figures check
    m = re.search(r"(\d+(\.\d+)?)", value_str.replace(",", ""))
    if not m:
        return None
    s = m.group(1)
    if "." in s:
        return len(s.strip("0").replace(".", ""))
    return len(s)

def approx_equal(a, b, tol=0.01):
    try:
        return abs(float(a) - float(b)) <= tol
    except:
        return False

def titration_expected_conc():
    # 25.0 mL HCl; 30.0 mL of 0.100 M NaOH; 1:1 reaction
    n_naoh = 0.100 * (30.0 / 1000)  # 0.00300 mol
    # n_HCl = n_NaOH
    c_hcl = n_naoh / (25.0 / 1000)  # 0.00300 / 0.0250 = 0.120 M
    return 0.120

# ---------- LLM FEEDBACK (OpenAI) ----------
def llm_feedback(answer, prompt, criteria, group, topic, band_target):
    """
    Uses OpenAI if OPENAI_API_KEY is set; otherwise returns a structured, decent fallback.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    criteria_joined = "\n- " + "\n- ".join(criteria)

    system = f"""
You are an experienced NSW HSC Chemistry marker.
Provide precise, criterion-referenced feedback (like Kevin Bio Bot).
Tone: encouraging, specific, exam-focused. Be concise but not superficial.
Return sections with clear headings: Strengths; Marks Lost (mapped to criteria); Exemplar Response; Next Steps (3 bullet points); Final Checklist.
Target group: {group}. Topic: {topic}. {band_target}
When applicable, mention units, significant figures, and explicit links back to the question.
"""
    user = f"""
QUESTION:
{prompt}

CRITERIA (marker points):
{criteria_joined}

STUDENT ANSWER:
{answer}
"""

    if api_key:
        try:
            # OpenAI Python SDK v1 style
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":system},
                    {"role":"user","content":user}
                ],
                temperature=0.3
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ LLM error: {e}\n\nFalling back to heuristic feedback...\n\n" + heuristic_feedback(answer, prompt, criteria, group, topic, band_target)
    else:
        return heuristic_feedback(answer, prompt, criteria, group, topic, band_target)

def heuristic_feedback(answer, prompt, criteria, group, topic, band_target):
    """Offline fallback: maps keywords to criteria and generates structured, useful feedback."""
    strengths = []
    misses = []
    for c in criteria:
        # simple keyword matching
        words = [w.lower() for w in re.findall(r"[A-Za-z]+", c)]
        covered = any(w in answer.lower() for w in words if len(w) > 4)
        if covered:
            strengths.append(c)
        else:
            misses.append(c)

    # calculation-specific nudge for the titration item
    calc_hint = ""
    if "titrated" in prompt.lower():
        expected = titration_expected_conc()
        has_number = re.search(r"([0-9]+(\.[0-9]+)?)", answer)
        if has_number:
            stated = float(has_number.group(1))
            if approx_equal(stated, expected, 0.01):
                calc_hint = "• Calculation appears numerically correct (≈0.120 M). Ensure units and sig. figs are stated.\n"
            else:
                calc_hint = f"• Expected ≈0.120 M based on n=CV and 1:1 stoichiometry; revisit steps and include units.\n"
        else:
            calc_hint = "• Provide a numerical answer with units; expected ≈0.120 M for this titration.\n"

    strengths_text = "\n".join([f"• {s}" for s in strengths]) or "• Clear attempt. Some relevant ideas present."
    misses_text = "\n".join([f"• {m}" for m in misses]) or "• Minor refinements only."

    exemplar = "A model answer would directly address each criterion in order, using correct terminology, explicit links to the question, and (where relevant) working, units, and appropriate significant figures."
    if "Le Chatelier" in prompt:
        exemplar = (
            "Because ammonia formation is exothermic, increasing temperature favours the endothermic reverse reaction. "
            "By Le Chatelier’s principle, the equilibrium shifts to oppose the temperature increase, so the position moves left, reducing the yield of ammonia. "
            "Thus, higher temperatures decrease NH₃ yield despite faster rates; optimal industrial conditions balance rate and yield."
        )
    if "titrated" in prompt.lower():
        exemplar = (
            "HCl + NaOH → NaCl + H₂O (1:1). n(NaOH)=0.100×0.0300=0.00300 mol; therefore n(HCl)=0.00300 mol. "
            "[HCl]=n/V=0.00300/0.0250=0.120 M (3 sig. figs) with units."
        )

    next_steps = [
        "Underline key verbs and plan a 2–3 sentence scaffold before writing.",
        "Add explicit links back to the question in your final sentence.",
        "Check units and significant figures; include a concluding statement."
    ]
    if "Band 4" in band_target:
        next_steps = [
            "Complete every required step (don’t leave half-answers).",
            "State units and show working clearly to avoid easy mark losses.",
            "Use the scaffold: State → Explain → Support with data/example → Conclude."
        ]
    if "avoid Band 2" in band_target:
        next_steps = [
            "Always write something relevant for each question (no blanks).",
            "Use correct definitions and simple, direct sentences.",
            "Practise 10–15 minute mini-sets to build confidence and accuracy."
        ]

    checklist = [
        "Did I answer every part of the question?",
        "Did I use correct terminology and units?",
        "Did I include a clear concluding/link-back sentence?"
    ]

    fb = [
        "### ✅ Strengths",
        strengths_text,
        "\n### ⚠️ Marks Lost (mapped to criteria)",
        misses_text,
        "\n### 🧠 Exemplar Response",
        exemplar,
        "\n### 🔧 Next Steps (do these on your next attempt)",
        "\n".join([f"• {s}" for s in next_steps]),
        "\n### ☑️ Final Checklist",
        "\n".join([f"• {c}" for c in checklist]),
    ]
    if calc_hint:
        fb.insert(4, f"**Calculation note**\n{calc_hint}")
    return "\n".join(fb)

# ---------- UI ----------
st.set_page_config(page_title=APP_TITLE, page_icon="🧪", layout="centered")
st.title(APP_TITLE)
st.write(INTRO)

with st.expander("How to use"):
    st.markdown("""
1) Choose your group (Top / Middle / Lower).  
2) Click **Get Question** → read the prompt & criteria.  
3) Write your answer and click **Get Feedback**.  
4) Review strengths/marks lost, read the exemplar, and follow the **3 next steps**.  
5) **Improve and Resubmit** to see your progress.
""")

group = st.selectbox("Choose your group", GROUPS)
topic_options = sorted({q["topic"] for q in QUESTION_BANK if q["group"] == group})
topic = st.selectbox("Choose a topic", topic_options)

if "current" not in st.session_state:
    st.session_state.current = None

colA, colB = st.columns(2)
with colA:
    if st.button("📝 Get Question"):
        candidates = [q for q in QUESTION_BANK if q["group"] == group and q["topic"] == topic]
        st.session_state.current = random.choice(candidates)

if st.session_state.current:
    q = st.session_state.current
    st.subheader("Question")
    st.write(q["prompt"])
    with st.expander("Marking criteria"):
        st.markdown("\n".join([f"- {c}" for c in q["criteria"]]))
        st.caption(q["band_target"])

    answer = st.text_area("Type your answer here", height=180)

    with colB:
        submit = st.button("🔍 Get Feedback")
    if submit and answer.strip():
        st.divider()
        st.subheader("Marker-style Feedback")
        feedback_text = llm_feedback(answer, q["prompt"], q["criteria"], q["group"], q["topic"], q["band_target"])
        st.markdown(feedback_text)

        st.info("Tip: Edit your answer below and click **Get Feedback** again to compare improvements.")
