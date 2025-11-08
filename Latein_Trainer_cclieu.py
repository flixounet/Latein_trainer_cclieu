import random
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Latin Trainer – CC de lieu & Deklinationen", page_icon="📜", layout="centered")

TITLE = "Latin Trainer – CC de lieu (Akkusativ/Ablativ/Lokativ) & Deklinationen"
st.title(TITLE)
st.caption("Niveau: 4e (collège). Enthält Lernkarten, Multiple-Choice und eine Grammatik-Spickkarte.")

# ---------- Session state init ----------
def ss_init():
    if "card_index" not in st.session_state: st.session_state.card_index = 0
    if "show_answer" not in st.session_state: st.session_state.show_answer = False
    if "known" not in st.session_state: st.session_state.known = 0
    if "unknown" not in st.session_state: st.session_state.unknown = 0
    if "mc_order" not in st.session_state:
        st.session_state.mc_order = list(range(len(MC_QUESTIONS)))
        random.shuffle(st.session_state.mc_order)
    if "mc_pos" not in st.session_state: st.session_state.mc_pos = 0
    if "mc_score" not in st.session_state: st.session_state.mc_score = 0
    if "mc_feedback" not in st.session_state: st.session_state.mc_feedback = ""
    if "finished" not in st.session_state: st.session_state.finished = False

# ---------- Content: flashcards & questions ----------
FLASHCARDS = [
    {"q": "Übersetze: Omnes viae Romam ducunt.",
     "a": "Alle Wege führen nach Rom. Grammatik: Romam = Akkusativ der Richtung (wohin?)."},
    {"q": "Regel: Wie drückst du Richtung zu einer Stadt aus?",
     "a": "Stadtname im Akkusativ ohne Präposition: Romam, Athenas, Carthaginem …"},
    {"q": "Regel: Wie drückst du den Ort (wo?) bei Städten aus?",
     "a": "Lokativ (ohne Präposition): Romae, Athenis; auch domi (zu Hause)."},
    {"q": "Regel: Wie drückst du den Ort (wo?) bei Gebäuden/Räumen aus?",
     "a": "in + Ablativ: in amphitheatro, in schola, in foro."},
    {"q": "Regel: Wie drückst du die Herkunft (woher?) aus?",
     "a": "ex/e, a/ab oder de + Ablativ: ex urbe, a Roma, de monte."},
    {"q": "Übersetze: Ars longa, vita brevis.",
     "a": "Die Kunst ist lang, das Leben ist kurz (‚ist‘ wird im Lateinischen oft ausgelassen)."},
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
    {
        "q": "Bestimme Kasus + Funktion: Romam",
        "options": [
            "Ablativ (Ort: wo?)",
            "Lokativ (Ort: wo?)",
            "Akkusativ der Richtung (wohin?)",
            "Genitiv (Besitz)"
        ],
        "answer": 2,
        "explain": "Städtenamen: Akkusativ ohne Präposition = Richtung → Romam (wohin?)."
    },
    {
        "q": "Wähle die korrekte Form: Senatores ___ sedent.",
        "options": ["Romam", "Romae", "Romā (Abl.)", "ad Romam"],
        "answer": 1,
        "explain": "Ort bei Städten = Lokativ → Romae (sie sitzen in Rom)."
    },
    {
        "q": "Gladiatores pugnant ___ amphitheatro.",
        "options": ["in (Akk.) – in amphitheatrum", "in (Abl.) – in amphitheatro", "ad amphitheatrum", "ex amphitheatro"],
        "answer": 1,
        "explain": "Ort (wo?) bei Gebäuden → in + Ablativ: in amphitheatro."
    },
    {
        "q": "Spectatores veniunt ___ urbe.",
        "options": ["in", "ad", "ex", "cum"],
        "answer": 2,
        "explain": "Herkunft (woher?) → ex + Ablativ: ex urbe."
    },
    {
        "q": "Discipuli intrant ___ scholam.",
        "options": ["in", "de", "e/ex", "cum"],
        "answer": 0,
        "explain": "Richtung (wohin?) → in + Akkusativ: in scholam."
    },
    {
        "q": "Übersetzung: Ars longa, vita brevis.",
        "options": [
            "Die Kunst ist lang, das Leben ist kurz.",
            "Die Kunst ist schwierig, das Leben ist schön.",
            "Alle Wege führen nach Rom.",
            "Die Lehrer sind streng, die Schüler sind müde."
        ],
        "answer": 0,
        "explain": "Klassisches Sprichwort: Ars longa, vita brevis."
    },
    {
        "q": "Endung –arum steht für …",
        "options": ["Genitiv Plural der 1. Deklination", "Akkusativ Singular der 1. Deklination",
                    "Nominativ Plural der 2. Deklination mask.", "Dativ/Ablativ Plural der 2. Deklination"],
        "answer": 0,
        "explain": "-arum = Gen. Pl. der 1. Deklination (puellarum)."
    },
    {
        "q": "servis ist …",
        "options": ["Dativ oder Ablativ Plural (2. Dekl.)", "Genitiv Singular (2. Dekl.)",
                    "Nominativ Plural (1. Dekl.)", "Akkusativ Singular (3. Dekl.)"],
        "answer": 0,
        "explain": "servis: Dat./Abl. Pl. (‚den/mit den Sklaven‘)."
    },
    {
        "q": "Wähle den richtigen Satz für ‚Ich bin in Rom.‘",
        "options": ["Romam sum.", "Romae sum.", "in Romam sum.", "ad Romam sum."],
        "answer": 1,
        "explain": "Ort bei Städten = Lokativ → Romae sum."
    },
    {
        "q": "Wähle den richtigen Satz für ‚Ich gehe nach Rom.‘",
        "options": ["Romae eo.", "in Roma eo.", "Romam eo.", "ex Roma eo."],
        "answer": 2,
        "explain": "Richtung zur Stadt → Akkusativ ohne Präposition: Romam eo."
    },
    {
        "q": "Athenis bedeutet …",
        "options": ["in Athen (Lokativ Pl.)", "nach Athen (Akk.)", "aus Athen (Abl.)", "bei Athen (Dativ)"],
        "answer": 0,
        "explain": "Athen ist Pluralwort; Athenis = Lokativ Plural → ‚in Athen‘."
    },
    {
        "q": "Welche Kombination drückt einen Ort (wo?) aus?",
        "options": ["in + Akkusativ", "in + Ablativ", "ad + Akkusativ", "ex + Ablativ"],
        "answer": 1,
        "explain": "Ort (wo?) bei Gebäuden → in + Ablativ."
    },
    {
        "q": "‚Omnes viae Romam ducunt‘: Welche Funktion hat Romam?",
        "options": ["Lokativ (Ort)", "Ablativ (Ort)", "Genitiv (Besitz)", "Akkusativ der Richtung (wohin)"],
        "answer": 3,
        "explain": "Romam = Akkusativ der Richtung (wohin?)."
    },
    {
        "q": "1. Dekl.: Nominativ Plural?",
        "options": ["-ae", "-as", "-arum", "-is"],
        "answer": 0,
        "explain": "Nom. Pl. 1. Dekl. = -ae (viae)."
    },
    {
        "q": "2. Dekl. mask.: Nominativ Plural?",
        "options": ["-i", "-os", "-um", "-is"],
        "answer": 0,
        "explain": "Nom. Pl. 2. Dekl. mask. = -i (servi)."
    },
]

CHEATSHEET = """
**Ablativ vs. Lokativ (Ort „wo?“)**  
- **Ablativ**: mit *in* → *in amphitheatro*, *in schola*. Gilt für Gebäude/Räume/Orte.  
- **Lokativ**: **ohne** Präposition, **nur** bei Städten und wenigen Wörtern wie *domi* → *Romae*, *Athenis*, *domi*.  
**Richtung (wohin?)**  
- Stadtname: Akkusativ **ohne** Präposition → *Romam*, *Athenas*.  
- Gebäude/Raum: *in + Akkusativ* → *in scholam*, *in amphitheatrum*.  
**Herkunft (woher?)**  
- *ex/e*, *a/ab*, *de* + Ablativ → *ex urbe*, *a Roma*, *de monte*.
"""

# ---------- UI layout ----------
tabs = st.tabs(["🃏 Lernkarten", "✅ Multiple-Choice", "📎 Grammatik-Spickkarte"])

ss_init()

# ---------- Tab 1: Flashcards ----------
with tabs[0]:
    st.subheader("Lernkarten (Q → A)")
    st.write("Klicke auf **Antwort zeigen** und markiere **gewusst** oder **nicht gewusst**.")

    card = FLASHCARDS[st.session_state.card_index]
    st.markdown(f"**Frage:** {card['q']}")

    colA, colB, colC = st.columns([1,1,1])
    with colA:
        if st.button("Antwort zeigen", use_container_width=True):
            st.session_state.show_answer = True
    with colB:
        if st.button("✅ Gewusst", type="primary", use_container_width=True):
            st.session_state.known += 1
            st.session_state.show_answer = False
            st.session_state.card_index = (st.session_state.card_index + 1) % len(FLASHCARDS)
    with colC:
        if st.button("❌ Nicht gewusst", use_container_width=True):
            st.session_state.unknown += 1
            st.session_state.show_answer = False
            # einfache Wiederholung: unbekannte Karte später erneut
            FLASHCARDS.append(card)
            st.session_state.card_index = (st.session_state.card_index + 1) % len(FLASHCARDS)

    if st.session_state.show_answer:
        st.info(f"**Antwort:** {card['a']}")

    st.progress((st.session_state.known) / max(1, (st.session_state.known + st.session_state.unknown)))
    st.caption(f"Gewusst: {st.session_state.known} · Nicht gewusst: {st.session_state.unknown}")

    if st.button("🔄 Fortschritt zurücksetzen"):
        st.session_state.card_index = 0
        st.session_state.show_answer = False
        st.session_state.known = 0
        st.session_state.unknown = 0
        st.experimental_rerun()

# ---------- Tab 2: Multiple-Choice ----------
with tabs[1]:
    st.subheader("Multiple-Choice-Quiz")
    if st.session_state.finished:
        st.success(f"Fertig! Score: {st.session_state.mc_score} / {len(MC_QUESTIONS)}")
        if st.button("↩️ Nochmal spielen"):
            st.session_state.mc_order = list(range(len(MC_QUESTIONS)))
            random.shuffle(st.session_state.mc_order)
            st.session_state.mc_pos = 0
            st.session_state.mc_score = 0
            st.session_state.mc_feedback = ""
            st.session_state.finished = False
            st.experimental_rerun()
    else:
        idx = st.session_state.mc_order[st.session_state.mc_pos]
        q = MC_QUESTIONS[idx]
        st.markdown(f"**Frage {st.session_state.mc_pos + 1} von {len(MC_QUESTIONS)}**")
        st.write(q["q"])

        choice = st.radio("Antwort wählen:", q["options"], index=None, label_visibility="collapsed")

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Antwort prüfen", type="primary", disabled=(choice is None)):
                if q["options"].index(choice) == q["answer"]:
                    st.session_state.mc_score += 1
                    st.session_state.mc_feedback = "✅ Richtig!"
                else:
                    correct_text = q["options"][q["answer"]]
                    st.session_state.mc_feedback = f"❌ Falsch. Richtig ist: **{correct_text}**"
        with col2:
            if st.button("Nächste Frage"):
                # Nur weiter, wenn Feedback schon erzeugt wurde oder ohne Prüfung weiterspringen
                st.session_state.mc_pos += 1
                st.session_state.mc_feedback = ""
                if st.session_state.mc_pos >= len(MC_QUESTIONS):
                    st.session_state.finished = True
                st.experimental_rerun()

        if st.session_state.mc_feedback:
            st.info(st.session_state.mc_feedback)
            st.caption(q["explain"])

        st.caption(f"Aktueller Score: {st.session_state.mc_score}")

# ---------- Tab 3: Cheat Sheet ----------
with tabs[2]:
    st.subheader("Grammatik – Ablativ vs. Lokativ & CC de lieu")
    st.markdown(CHEATSHEET)
    with st.expander("Deklination – wichtige Endungen (Kurzüberblick)"):
        st.markdown("""
**1. Deklination (meist fem.)**  
- Sg.: -a, -ae, -ae, -am, -a  
- Pl.: -ae, -arum, -is, -as, -is  

**2. Deklination (mask./neutr.)**  
- mask. Sg.: -us/-er, -i, -o, -um, -o · Pl.: -i, -orum, -is, -os, -is  
- neutr. Sg.: -um, -i, -o, -um, -o · Pl.: -a, -orum, -is, -a, -is
""")
