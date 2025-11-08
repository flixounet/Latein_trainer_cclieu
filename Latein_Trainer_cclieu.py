# latein_trainer_cclieu.py
import random
import streamlit as st

# ---------------- Page setup ----------------
st.set_page_config(page_title="Latin Trainer – CC de lieu & Deklinationen", page_icon="📜", layout="centered")
st.title("Latin Trainer – CC de lieu (Akkusativ/Ablativ/Lokativ) & Deklinationen")
st.caption("Niveau 4e (collège). Lernkarten, Multiple-Choice und Spickzettel. Stabil für neue Streamlit-Versionen.")

# ---------------- Content ----------------
FLASHCARDS = [
    {"q": "Übersetze: Omnes viae Romam ducunt.",
     "a": "Alle Wege führen nach Rom. Grammatik: Romam = Akkusativ der Richtung (wohin?)."},
    {"q": "Regel: Richtung zu einer Stadt?",
     "a": "Stadtname im Akkusativ ohne Präposition: Romam, Athenas, Carthaginem …"},
    {"q": "Regel: Ort (wo?) bei Städten?",
     "a": "Lokativ (ohne Präposition): Romae, Athenis; außerdem domi (zu Hause)."},
    {"q": "Regel: Ort (wo?) bei Gebäuden/Räumen?",
     "a": "in + Ablativ: in amphitheatro, in schola, in foro."},
    {"q": "Regel: Herkunft (woher?)?",
     "a": "ex/e, a/ab oder de + Ablativ: ex urbe, a Roma, de monte."},
    {"q": "Übersetze: Ars longa, vita brevis.",
     "a": "Die Kunst ist lang, das Leben ist kurz (‚est‘ wird oft ausgelassen)."},
    {"q": "1. Deklination: Nominativ Plural?",
     "a": "-ae (viae, puellae)."},
    {"q": "1. Deklination: Genitiv Plural?",
     "a": "-arum (puellarum)."},
    {"q": "1. Deklination: Akkusativ Singular?",
     "a": "-am (viam, puellam)."},
    {"q": "1. Deklination: Ablativ Singular?",
     "a": "-a (via, puella)."},
    {"q": "2. Deklination mask.: Nominativ Plural?",
     "a": "-i (servi, amici)."},
    {"q": "2. Deklination: Dativ/Ablativ Plural?",
     "a": "-is (servis, templis)."},
    {"q": "Bedeutung von ‚in + Akkusativ‘?",
     "a": "Richtung/Wohin? → in scholam, in amphitheatrum (hinein)."},
    {"q": "Bedeutung von ‚in + Ablativ‘?",
     "a": "Ort/Wo? → in schola, in amphitheatro (drin)."},
]

MC_QUESTIONS = [
    {"q": "Bestimme Kasus + Funktion: Romam",
     "options": ["Ablativ (Ort: wo?)", "Lokativ (Ort: wo?)", "Akkusativ der Richtung (wohin?)", "Genitiv (Besitz)"],
     "answer": 2, "explain": "Städtename im Akkusativ ohne Präposition = Richtung → Romam (wohin?)."},
    {"q": "Wähle die korrekte Form: Senatores ___ sedent.",
     "options": ["Romam", "Romae", "Romā (Abl.)", "ad Romam"],
     "answer": 1, "explain": "Ort bei Städten = Lokativ → Romae (sie sitzen in Rom)."},
    {"q": "Gladiatores pugnant ___ amphitheatro.",
     "options": ["in (Akk.) – in amphitheatrum", "in (Abl.) – in amphitheatro", "ad amphitheatrum", "ex amphitheatro"],
     "answer": 1, "explain": "Ort (wo?) → in + Ablativ: in amphitheatro."},
    {"q": "Spectatores veniunt ___ urbe.",
     "options": ["in", "ad", "ex", "cum"],
     "answer": 2, "explain": "Herkunft (woher?) → ex + Ablativ: ex urbe."},
    {"q": "Discipuli intrant ___ scholam.",
     "options": ["in", "de", "e/ex", "cum"],
     "answer": 0, "explain": "Richtung (wohin?) → in + Akkusativ: in scholam."},
    {"q": "Übersetzung: Ars longa, vita brevis.",
     "options": ["Die Kunst ist lang, das Leben ist kurz.", "Die Kunst ist schwierig, das Leben ist schön.",
                 "Alle Wege führen nach Rom.", "Die Lehrer sind streng, die Schüler sind müde."],
     "answer": 0, "explain": "Klassisches Sprichwort."},
    {"q": "Endung –arum steht für …",
     "options": ["Genitiv Plural der 1. Deklination", "Akkusativ Singular der 1. Deklination",
                 "Nominativ Plural der 2. Deklination mask.", "Dativ/Ablativ Plural der 2. Deklination"],
     "answer": 0, "explain": "-arum = Gen. Pl. 1. Dekl."},
    {"q": "servis ist …",
     "options": ["Dativ oder Ablativ Plural (2. Dekl.)", "Genitiv Singular (2. Dekl.)",
                 "Nominativ Plural (1. Dekl.)", "Akkusativ Singular (3. Dekl.)"],
     "answer": 0, "explain": "servis: Dat./Abl. Pl. (‚den/mit den Sklaven‘)."},
    {"q": "Wähle den richtigen Satz für ‚Ich bin in Rom.‘",
     "options": ["Romam sum.", "Romae sum.", "in Romam sum.", "ad Romam sum."],
     "answer": 1, "explain": "Ort bei Städten = Lokativ → Romae sum."},
    {"q": "Wähle den richtigen Satz für ‚Ich gehe nach Rom.‘",
     "options": ["Romae eo.", "in Roma eo.", "Romam eo.", "ex Roma eo."],
     "answer": 2, "explain": "Richtung zur Stadt → Akkusativ ohne Präposition: Romam eo."},
    {"q": "Athenis bedeutet …",
     "options": ["in Athen (Lokativ Pl.)", "nach Athen (Akk.)", "aus Athen (Abl.)", "bei Athen (Dativ)"],
     "answer": 0, "explain": "Athenis = Lokativ Plural → ‚in Athen‘."},
    {"q": "Welche Kombination drückt einen Ort (wo?) aus?",
     "options": ["in + Akkusativ", "in + Ablativ", "ad + Akkusativ", "ex + Ablativ"],
     "answer": 1, "explain": "Ort (wo?) → in + Ablativ."},
    {"q": "‚Omnes viae Romam ducunt‘: Welche Funktion hat Romam?",
     "options": ["Lokativ (Ort)", "Ablativ (Ort)", "Genitiv (Besitz)", "Akkusativ der Richtung (wohin)"],
     "answer": 3, "explain": "Romam = Akkusativ der Richtung."},
    {"q": "1. Dekl.: Nominativ Plural?",
     "options": ["-ae", "-as", "-arum", "-is"],
     "answer": 0, "explain": "Nom. Pl. 1. Dekl. = -ae."},
    {"q": "2. Dekl. mask.: Nominativ Plural?",
     "options": ["-i", "-os", "-um", "-is"],
     "answer": 0, "explain": "Nom. Pl. 2. Dekl. mask. = -i."},
]

CHEATSHEET = """
**Ablativ vs. Lokativ (Ort „wo?“)**  
- **Ablativ**: mit *in* → *in amphitheatro*, *in schola*. (Gebäude/Räume/Orte)  
- **Lokativ**: **ohne** Präposition, **nur** bei Städten und *domi* → *Romae*, *Athenis*, *domi*.  

**Richtung (wohin?)**  
- Stadtname: Akkusativ **ohne** Präposition → *Romam*, *Athenas*.  
- Gebäude/Raum: *in + Akkusativ* → *in scholam*, *in amphitheatrum*.  

**Herkunft (woher?)**  
- *ex/e*, *a/ab*, *de* + Ablativ → *ex urbe*, *a Roma*, *de monte*.
"""

# ---------------- Session helpers ----------------
def init_quiz_state():
    """Robuste Initialisierung / Heilung des MC-States."""
    n = len(MC_QUESTIONS)
    if "mc_order" not in st.session_state or not isinstance(st.session_state.mc_order, list) or len(st.session_state.mc_order) != n:
        st.session_state.mc_order = list(range(n))
        random.shuffle(st.session_state.mc_order)
    if "mc_pos" not in st.session_state or not isinstance(st.session_state.mc_pos, int) or st.session_state.mc_pos < 0:
        st.session_state.mc_pos = 0
    if st.session_state.mc_pos >= n:
        st.session_state.mc_pos = n - 1 if n > 0 else 0
    if "mc_score" not in st.session_state: st.session_state.mc_score = 0
    if "mc_feedback" not in st.session_state: st.session_state.mc_feedback = ""
    if "finished" not in st.session_state: st.session_state.finished = False

def init_cards_state():
    if "card_index" not in st.session_state: st.session_state.card_index = 0
    if "show_answer" not in st.session_state: st.session_state.show_answer = False
    if "known" not in st.session_state: st.session_state.known = 0
    if "unknown" not in st.session_state: st.session_state.unknown = 0

init_cards_state()
init_quiz_state()

# ---------------- Tabs ----------------
tabs = st.tabs(["🃏 Lernkarten", "✅ Multiple-Choice", "📎 Spickkarte"])

# -------- Tab 1: Flashcards --------
with tabs[0]:
    st.subheader("Lernkarten (Q → A)")
    card = FLASHCARDS[st.session_state.card_index]
    st.markdown(f"**Frage:** {card['q']}")

    c1, c2, c3 = st.columns(3)
    if c1.button("Antwort zeigen"):
        st.session_state.show_answer = True
    if c2.button("✅ Gewusst"):
        st.session_state.known += 1
        st.session_state.show_answer = False
        st.session_state.card_index = (st.session_state.card_index + 1) % len(FLASHCARDS)
        st.rerun()
    if c3.button("❌ Nicht gewusst"):
        st.session_state.unknown += 1
        st.session_state.show_answer = False
        # Karte ans Ende hängen (sanfte Wiederholung)
        FLASHCARDS.append(card)
        st.session_state.card_index = (st.session_state.card_index + 1) % len(FLASHCARDS)
        st.rerun()

    if st.session_state.show_answer:
        st.info(f"**Antwort:** {card['a']}")

    total = st.session_state.known + st.session_state.unknown
    st.progress((st.session_state.known / total) if total else 0.0, text="Anteil gewusst")

    if st.button("🔄 Fortschritt zurücksetzen"):
        for k in ["card_index", "show_answer", "known", "unknown"]:
            if k in st.session_state: del st.session_state[k]
        init_cards_state()
        st.rerun()

# -------- Tab 2: Multiple-Choice --------
with tabs[1]:
    st.subheader("Multiple-Choice-Quiz")

    n = len(MC_QUESTIONS)
    if n == 0:
        st.error("Keine Fragen vorhanden.")
    elif st.session_state.finished:
        st.success(f"Fertig! Score: {st.session_state.mc_score} / {n}")
        if st.button("↩️ Nochmal spielen"):
            for k in ["mc_order", "mc_pos", "mc_score", "mc_feedback", "finished"]:
                if k in st.session_state: del st.session_state[k]
            init_quiz_state()
            st.rerun()
    else:
        idx = st.session_state.mc_order[st.session_state.mc_pos]
        q = MC_QUESTIONS[idx]

        st.markdown(f"**Frage {st.session_state.mc_pos + 1} von {n}**")
        st.write(q["q"])

        # Platzhalter sichert gegen None/IndexError ab
        options = ["— bitte wählen —"] + q["options"]
        choice = st.selectbox("Antwort wählen:", options, index=0, label_visibility="collapsed")

        colA, colB = st.columns(2)
        if colA.button("Antwort prüfen", type="primary"):
            if choice != options[0]:
                is_correct = (q["options"][options.index(choice) - 1] == q["options"][q["answer"]])
                if is_correct:
                    st.session_state.mc_score += 1
                    st.session_state.mc_feedback = "✅ Richtig!"
                else:
                    st.session_state.mc_feedback = f"❌ Falsch. Richtig ist: **{q['options'][q['answer']]}**"
            else:
                st.session_state.mc_feedback = "ℹ️ Bitte zuerst eine Antwort wählen."
            st.rerun()

        if colB.button("Nächste Frage ➜"):
            st.session_state.mc_pos += 1
            st.session_state.mc_feedback = ""
            if st.session_state.mc_pos >= n:
                st.session_state.finished = True
            st.rerun()

        if st.session_state.mc_feedback:
            st.info(st.session_state.mc_feedback)
            st.caption(q["explain"])
        st.caption(f"Aktueller Score: {st.session_state.mc_score}")

# -------- Tab 3: Cheat Sheet --------
with tabs[2]:
    st.subheader("Ablativ vs. Lokativ & CC de lieu")
    st.markdown(CHEATSHEET)
    with st.expander("Deklinationen – Kurzüberblick"):
        st.markdown("""
**1. Deklination (meist fem.)**  
- Sg.: -a, -ae, -ae, -am, -a  
- Pl.: -ae, -arum, -is, -as, -is  

**2. Deklination (mask./neutr.)**  
- mask. Sg.: -us/-er, -i, -o, -um, -o · Pl.: -i, -orum, -is, -os, -is  
- neutr. Sg.: -um, -i, -o, -um, -o · Pl.: -a, -orum, -is, -a, -is
""")
