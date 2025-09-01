import os
import re
import random
import streamlit as st

# ----------------------------
# App config
# ----------------------------
st.set_page_config(page_title="🧪 Chem Bot — HSC Exam Coach", page_icon="🧪", layout="centered")
st.title("🧪 Chem Bot — HSC Exam Coach")
st.write("Targeted past-paper style questions with marker-style feedback, an exemplar response, and step-by-step coaching to build stronger answers.")

# ----------------------------
# Question bank
#  - Paraphrased, HSC-style items covering Modules 5–8
#  - group: Top (Band 5/6), Middle (Band 4 security), Lower (limit Band 2)
# ----------------------------
QUESTION_BANK = [
    # =======================
    # MODULE 5 — Equilibrium & Acid Reactions
    # =======================
    {
        "module": "Module 5 — Equilibrium & Acid Reactions",
        "group": "Top (Band 5/6)",
        "topic": "Haber equilibrium & temperature",
        "prompt": "Explain, using Le Chatelier’s principle, how increasing temperature affects the equilibrium yield of ammonia in the Haber process. (6 marks)",
        "criteria": [
            "Identifies forward ammonia formation as exothermic.",
            "States correct direction of shift when temperature increases (towards endothermic direction).",
            "Explains why: added heat favours the endothermic reaction to oppose the change.",
            "Links shift explicitly to ammonia yield (decreases).",
            "Uses correct terminology; avoids vague language.",
            "Finishes with a concise concluding sentence tied to the question."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "module": "Module 5 — Equilibrium & Acid Reactions",
        "group": "Top (Band 5/6)",
        "topic": "Kc interpretation",
        "prompt": "A(aq) + B(aq) ⇌ C(aq). At 25 °C, Kc = 8.0. Discuss what this value implies about the position of equilibrium and how doubling [A] initially (with B constant) affects the initial reaction quotient, Q. (5–6 marks)",
        "criteria": [
            "Interprets Kc>1 as products favoured at equilibrium.",
            "Defines Q and relates it to current concentrations.",
            "Explains the effect of doubling [A] on Q (Q increases).",
            "Predicts direction of change to re-establish equilibrium (shifts right).",
            "Uses clear logic and correct terminology."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "module": "Module 5 — Equilibrium & Acid Reactions",
        "group": "Middle (Band 4 security)",
        "topic": "Weak acid pH estimate",
        "prompt": "A weak monoprotic acid HA has concentration 0.10 M with Ka = 1.8×10⁻⁵ at 25 °C. Estimate the pH, stating any assumptions. (3–4 marks)",
        "criteria": [
            "Sets up Ka = [H+][A−]/[HA] and weak acid approximation.",
            "Solves for [H+] (x ≈ √(Ka·C)).",
            "Calculates pH correctly (≈ 2.87).",
            "States assumption that x ≪ C (validity)."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },
    {
        "module": "Module 5 — Equilibrium & Acid Reactions",
        "group": "Lower (limit Band 2)",
        "topic": "Le Chatelier basics",
        "prompt": "State what Le Chatelier’s principle predicts when the temperature of an exothermic reaction mixture at equilibrium is increased. (1–2 marks)",
        "criteria": [
            "States system shifts to oppose the change (towards endothermic direction).",
            "Links to a decrease in yield of exothermic products."
        ],
        "band_target": "Goal: Lift to Band 3; avoid Band 2."
    },

    # =======================
    # MODULE 6 — Acid/Base Reactions
    # =======================
    {
        "module": "Module 6 — Acid/Base Reactions",
        "group": "Top (Band 5/6)",
        "topic": "Titration curve analysis",
        "prompt": "A weak acid is titrated with a strong base. Describe the key features of the pH curve, identify a suitable indicator, and justify your choice. (6 marks)",
        "criteria": [
            "Identifies initial pH > that of strong acid; buffer region present.",
            "Notes equivalence point pH > 7 for weak acid/strong base.",
            "Describes steep region around equivalence.",
            "Selects appropriate indicator with transition near equivalence pH.",
            "Justifies indicator choice referencing curve profile."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "module": "Module 6 — Acid/Base Reactions",
        "group": "Middle (Band 4 security)",
        "topic": "Strong acid–base titration",
        "prompt": "25.0 mL of HCl is completely neutralised by 30.0 mL of 0.100 M NaOH. Calculate the concentration of HCl. (3 marks)",
        "criteria": [
            "Balanced equation: HCl + NaOH → NaCl + H2O (1:1).",
            "Correct moles of NaOH (n = C×V in L).",
            "Correct [HCl] = n/V with units and sensible significant figures (≈0.120 M)."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },
    {
        "module": "Module 6 — Acid/Base Reactions",
        "group": "Lower (limit Band 2)",
        "topic": "pH basics",
        "prompt": "Define pH and state what a low pH indicates about a solution. (1–2 marks)",
        "criteria": [
            "Defines pH in terms of hydrogen ion concentration.",
            "States that low pH indicates high [H+] (acidic)."
        ],
        "band_target": "Goal: Lift to Band 3; avoid Band 2."
    },

    # =======================
    # MODULE 7 — Organic Chemistry
    # =======================
    {
        "module": "Module 7 — Organic Chemistry",
        "group": "Top (Band 5/6)",
        "topic": "Reaction pathways",
        "prompt": "Devise a reaction pathway to convert ethene to ethanoic acid. Include reagents/conditions and discuss regioselectivity or intermediate steps where relevant. (6 marks)",
        "criteria": [
            "Outlines hydration of ethene to ethanol (H2O/H+; suitable conditions).",
            "Oxidation of ethanol to ethanoic acid (e.g., KMnO4 or dichromate; acidic conditions).",
            "Mentions intermediate(s) and conditions clearly.",
            "Discusses selectivity/side reactions where relevant.",
            "Uses correct organic terminology and structural reasoning."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "module": "Module 7 — Organic Chemistry",
        "group": "Middle (Band 4 security)",
        "topic": "Empirical formula (combustion)",
        "prompt": "A 0.780 g sample of an unknown hydrocarbon is burned completely to form 2.64 g CO2 and 1.08 g H2O. Determine the empirical formula. (4–5 marks)",
        "criteria": [
            "Converts CO2 to moles C; H2O to moles H.",
            "Determines moles of C and H in sample.",
            "Finds simplest whole-number ratio.",
            "States empirical formula clearly (e.g., CH)."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },
    {
        "module": "Module 7 — Organic Chemistry",
        "group": "Lower (limit Band 2)",
        "topic": "Functional groups",
        "prompt": "Name the functional group present in ethanol and in ethanoic acid. (1–2 marks)",
        "criteria": [
            "Ethanol: hydroxyl (alcohol) group.",
            "Ethanoic acid: carboxyl group."
        ],
        "band_target": "Goal: Lift to Band 3; avoid Band 2."
    },

    # =======================
    # MODULE 8 — Applying Chemical Ideas
    # =======================
    {
        "module": "Module 8 — Applying Chemical Ideas",
        "group": "Top (Band 5/6)",
        "topic": "Spectroscopy (IR/MS/NMR) synthesis",
        "prompt": "A compound with molecular ion peak at m/z 60 shows a strong IR absorption near 1715 cm⁻¹ and an NMR quartet at δ ~4.1 (2H) with a triplet at δ ~1.3 (3H). Propose a structure and justify using the data. (6 marks)",
        "criteria": [
            "Interprets M⁺ peak (molecular mass).",
            "Uses IR ~1715 cm⁻¹ to infer carbonyl (likely ester/ketone).",
            "Uses NMR splitting/chemical shift to assign –OCH2–CH3 pattern (quartet + triplet).",
            "Proposes plausible structure (e.g., ethyl formate/acetate where consistent).",
            "Links each data point to the structure explicitly."
        ],
        "band_target": "Aim: Secure high Band 5 / push to Band 6."
    },
    {
        "module": "Module 8 — Applying Chemical Ideas",
        "group": "Middle (Band 4 security)",
        "topic": "Qualitative analysis plan",
        "prompt": "Outline a simple plan to identify the cation in an unknown salt using flame tests and precipitation reactions. (4 marks)",
        "criteria": [
            "Describes safe flame test procedure and indicates expected colours (e.g., Na⁺ yellow, K⁺ lilac, Ca²⁺ brick-red).",
            "Explains use of precipitating reagents (e.g., NaOH, NH3) to form characteristic hydroxides/complexes.",
            "States observation → inference logic.",
            "Mentions confirmatory test or repetition for reliability."
        ],
        "band_target": "Goal: Maximise chance of Band 4."
    },
    {
        "module": "Module 8 — Applying Chemical Ideas",
        "group": "Lower (limit Band 2)",
        "topic": "Test selection",
        "prompt": "Which simple test could you use to distinguish between a carbonate and a chloride salt? State the expected observation. (1–2 marks)",
        "criteria": [
            "Adds acid to carbonate → effervescence (CO2).",
            "No gas with chloride under same conditions."
        ],
        "band_target": "Goal: Lift to Band 3; avoid Band 2."
    },
]

GROUPS = ["Top (Band 5/6)", "Middle (Band 4 security)", "Lower (limit Band 2)"]
MODULES = sorted(set(q["module"] for q in QUESTION_BANK))

# ----------------------------
# Helpers (light heuristics for a few calc items)
# ----------------------------
def approx_equal(a, b, tol=0.02):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

def titration_expected_conc():
    # 25.0 mL HCl neutralised by 30.0 mL 0.100 M NaOH → [HCl] ≈ 0.120 M
    n_naoh = 0.100 * (30.0 / 1000.0)  # 0.00300 mol
    c_hcl = n_naoh / (25.0 / 1000.0)  # 0.120 M
    return 0.120

# ----------------------------
# Build-it-up coach (identify → describe → explain → conclude)
# ----------------------------
def build_it_up_steps(prompt: str):
    p = prompt.lower()
    if "haber" in p or "le chatelier" in p or "equilibrium" in p:
        return [
            "Identify: state which direction is exothermic vs endothermic.",
            "Describe: say which way equilibrium shifts when the change happens.",
            "Explain: why that shift opposes the change (link to energy/particles).",
            "Conclude: state the impact on yield clearly."
        ]
    if "titration curve" in p or "indicator" in p:
        return [
            "Identify: the acid/base strength and expected equivalence pH.",
            "Describe: key curve regions (initial, buffer/gradual, steep rise, equivalence).",
            "Explain: indicator choice by matching transition range to equivalence pH.",
            "Conclude: summarise the suitability of the indicator."
        ]
    if "neutralised" in p or "titrated" in p:
        return [
            "Identify: balanced equation and mole ratio.",
            "Describe: calculate moles using n = C×V (convert mL→L).",
            "Explain: link moles at endpoint to unknown concentration.",
            "Conclude: report concentration with units and sensible sig. figs."
        ]
    if "empirical formula" in p or "burned" in p:
        return [
            "Identify: moles of C from CO2 and H from H2O.",
            "Describe: determine moles of each element in the sample.",
            "Explain: find the simplest whole-number ratio.",
            "Conclude: write the empirical formula clearly."
        ]
    if "spectroscopy" in p or "ir" in p or "nmr" in p or "mass spectrum" in p:
        return [
            "Identify: molecular mass (M⁺) and key IR bands.",
            "Describe: NMR splitting/chemical shift patterns.",
            "Explain: link evidence to fragments/functional groups.",
            "Conclude: propose a structure that fits all data."
        ]
    if "qualitative" in p or "identify the cation" in p or "flame test" in p:
        return [
            "Identify: initial simple tests (flame colours).",
            "Describe: precipitation/complexation steps and observations.",
            "Explain: how each observation narrows the possibilities.",
            "Conclude: state the most likely ion and confirmatory step."
        ]
    if "carbonate" in p and "chloride" in p:
        return [
            "Identify: the reagent to distinguish (e.g., dilute acid).",
            "Describe: observation with carbonate (bubbles of gas).",
            "Explain: gas is CO₂ from acid–carbonate reaction.",
            "Conclude: chloride shows no effervescence under same conditions."
        ]
    # default scaffold
    return [
        "Identify: name the key concept/feature.",
        "Describe: state what happens or what the data shows.",
        "Explain: why it happens using correct terms.",
        "Conclude: link back to the question in one sentence."
    ]

# ----------------------------
# Feedback generation
#  - Uses OpenAI if OPENAI_API_KEY is set; otherwise uses heuristic fallback
# ----------------------------
def llm_feedback(answer: str, q: dict):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    criteria_text = "\n- " + "\n- ".join(q["criteria"])
    build_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(build_it_up_steps(q["prompt"]))])

    system = f"""
You are an experienced NSW HSC Chemistry marker.
Tone: warm, specific, encouraging, and student-friendly.
Return these EXACT sections, in this order, with short, useful paragraphs or bullets:

### ✅ Strengths
### ⚠️ Marks Lost (mapped to criteria)
### 🧱 Build It Up
### 🧠 Exemplar Response
### 🔧 Next Steps (3 bullet points)
### ☑️ Final Checklist

Keep it concise but not superficial. Use correct terminology, mention units/sig figs when relevant,
and always link back to the question. Aim to feel like a real teacher.
Target group: {q['group']}. Topic: {q['topic']}. {q['band_target']}
"""

    user = f"""
QUESTION:
{q['prompt']}

CRITERIA:
{criteria_text}

COACHING STEPS:
{build_text}

STUDENT ANSWER:
{answer}
"""

    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI()  # reads key from env var
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=0.2,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ LLM error: {e}\n\n" + heuristic_feedback(answer, q, build_text)
    else:
        return heuristic_feedback(answer, q, build_text)

def heuristic_feedback(answer: str, q: dict, build_text: str):
    strengths, misses = [], []
    for c in q["criteria"]:
        words = [w.lower() for w in re.findall(r"[A-Za-z]+", c)]
        covered = any(w in answer.lower() for w in words if len(w) > 4)
        (strengths if covered else misses).append(c)

    # quick, targeted note for the classic strong acid–base titration item
    calc_note = ""
    if "neutralised" in q["prompt"].lower() or "titrated" in q["prompt"].lower():
        expected = titration_expected_conc()
        num = re.search(r"([0-9]+(\.[0-9]+)?)", answer)
        if num and approx_equal(num.group(1), expected, 0.02):
            calc_note = "• Your numerical result is close to the expected ≈0.120 M. Include units and appropriate significant figures."
        else:
            calc_note = "• Expected ≈0.120 M using n=CV and a 1:1 ratio. Show working, include units, and use sensible significant figures."

    # exemplar (brief, pointed)
    exemplar = "A complete response will address each listed criterion clearly, using correct terminology and, where needed, working, units, and appropriate significant figures."
    if "hab" in q["prompt"].lower() or "le chatelier" in q["prompt"].lower():
        exemplar = ("Because the forward reaction forming ammonia is exothermic, increasing temperature favours the endothermic reverse reaction. "
                    "By Le Chatelier’s principle, the system shifts left to absorb the added heat, decreasing the yield of ammonia.")
    if "neutralised" in q["prompt"].lower() or "titrated" in q["prompt"].lower():
        exemplar = ("HCl + NaOH → NaCl + H₂O (1:1). n(NaOH)=0.100×0.0300=0.00300 mol; thus n(HCl)=0.00300 mol. "
                    "[HCl]=n/V=0.00300/0.0250=0.120 M (3 s.f.), with units.")
    if "empirical formula" in q["prompt"].lower():
        exemplar = ("Find moles of C from CO₂ and H from H₂O, determine simplest ratio, and state the empirical formula clearly (e.g., CH).")
    if "spectros" in q["prompt"].lower() or "ir" in q["prompt"].lower() or "nmr" in q["prompt"].lower():
        exemplar = ("Use M⁺ to deduce molecular mass; IR ~1715 cm⁻¹ for C=O; NMR quartet (~4.1, 2H) and triplet (~1.3, 3H) suggest –OCH₂–CH₃. "
                    "Propose an ester consistent with all data and justify.")

    # next steps tuned to band target
    next_steps = [
        "Plan your response with 2–3 bullet points before writing.",
        "Add a final sentence that links your explanation back to the question.",
        "Check units/significant figures where relevant."
    ]
    if "Band 4" in q["band_target"]:
        next_steps = [
            "Complete every step (identify → describe → explain → conclude).",
            "Always show working and include units to avoid easy mark losses.",
            "Use short, clear sentences with correct terms."
        ]
    if "avoid Band 2" in q["band_target"]:
        next_steps = [
            "Always write something relevant for each part — no blanks.",
            "Use correct definitions and simple, direct sentences.",
            "Practise short 10–15 minute sets to build accuracy."
        ]

    strengths_text = "\n".join([f"• {s}" for s in strengths]) or "• Some relevant ideas present."
    misses_text = "\n".join([f"• {m}" for m in misses]) or "• Only minor refinements needed."

    blocks = [
        "### ✅ Strengths",
        strengths_text,
        "\n### ⚠️ Marks Lost (mapped to criteria)",
        misses_text,
        "\n### 🧱 Build It Up",
        "\n".join([f"{i+1}. {s}" for i, s in enumerate(build_it_up_steps(q['prompt']))]),
        "\n### 🧠 Exemplar Response",
        exemplar,
        "\n### 🔧 Next Steps (do these on your next attempt)",
        "\n".join([f"• {s}" for s in next_steps]),
        "\n### ☑️ Final Checklist",
        "• Did I answer every part of the question?\n• Did I use correct terminology and (if relevant) units/sig. figs?\n• Did I include a clear concluding/link-back sentence?"
    ]
    if calc_note:
        blocks.insert(4, f"**Calculation note**\n{calc_note}")
    return "\n".join(blocks)

# ----------------------------
# UI
# ----------------------------
with st.expander("How to use"):
    st.markdown("""
1) Choose your **module** and **group**.  
2) Click **Get Question**, read the prompt & criteria.  
3) Write your answer and click **Get Feedback**.  
4) Read **Strengths**, **Marks Lost**, **Build It Up**, and the **Exemplar**.  
5) Improve and click **Get Feedback** again to see progress.
""")

module = st.selectbox("Choose module", MODULES)
group = st.selectbox("Choose group", GROUPS)

topics = sorted(set(q["topic"] for q in QUESTION_BANK if q["module"] == module and q["group"] == group))
topic = st.selectbox("Choose topic", topics)

if "current_q" not in st.session_state:
    st.session_state.current_q = None

cols = st.columns(2)
with cols[0]:
    if st.button("📝 Get Question"):
        candidates = [q for q in QUESTION_BANK if q["module"] == module and q["group"] == group and q["topic"] == topic]
        st.session_state.current_q = random.choice(candidates) if candidates else None

if st.session_state.current_q:
    q = st.session_state.current_q
    st.subheader("Question")
    st.write(q["prompt"])

    with st.expander("Marking criteria"):
        st.markdown("\n".join([f"- {c}" for c in q["criteria"]]))
        st.caption(q["band_target"])

    answer = st.text_area("Type your answer here", height=200)

    with cols[1]:
        submit = st.button("🔍 Get Feedback")

    if submit and answer.strip():
        st.divider()
        st.subheader("Marker-style Feedback")
        fb = llm_feedback(answer, q)
        st.markdown(fb)
        st.info("Tip: Edit your answer and click **Get Feedback** again to compare improvements.")
else:
    st.caption("Choose module/group/topic and click **Get Question** to begin.")
