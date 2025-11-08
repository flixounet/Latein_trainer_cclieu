import os
import json
import time
import random
import streamlit as st

# ---------------------- Page setup ----------------------
st.set_page_config(page_title="Latin Trainer – CC de lieu & Deklinationen", page_icon="📜", layout="centered")
st.title("Latin Trainer – CC de lieu (Akkusativ/Ablativ/Lokativ) & Deklinationen")
st.caption("Niveau: 4e (collège). Lernkarten, Multiple-Choice, Arcade-Quiz und Grammatik-Spickkarte.")

def _rerun():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

# ---------------------- Content ----------------------
FLASHCARDS = [
    {"q": "Übersetze: Omnes viae Romam ducunt.",
     "a": "Alle Wege führen nach Rom. (Romam = Akkusativ der Richtung: wohin?)"},
    {"q": "Regel: Richtung zu einer Stadt?",
     "a": "Stadtname im Akkusativ ohne Präposition: Romam, Athenas, Carthaginem …"},
    {"q": "Regel: Ort (wo?) bei Städten?",
     "a": "Lokativ ohne Präposition: Romae, Athenis; auch domi (zu Hause)."},
    {"q": "Regel: Ort (wo?) bei Gebäuden/Räumen?",
     "a": "in + Ablativ: in amphitheatro, in schola, in foro."},
    {"q": "Regel: Herkunft (woher?)?",
     "a": "ex/e, a/ab oder de + Ablativ: ex urbe, a Roma, de monte."},
    {"q": "Übersetze: Ars longa, vita brevis.",
     "a": "Die Kunst ist lang, das Leben ist kurz. („est“ wird oft ausgelassen)."},
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
    {"q": "Bedeutung von „in + Akkusativ“?",
     "a": "Richtung/Wohin? → in scholam, in amphitheatrum (hinein)."},
    {"q": "Bedeutung von „in + Ablativ“?",
     "a": "Ort/Wo? → in schola, in amphitheatro (drin)."},
    {"q": "Was bedeutet Romae?",
     "a": "In Rom (Lokativ)."},
    {"q": "Was bedeutet Romam?",
     "a": "Nach Rom (Akkusativ der Richtung)."},
]

MC_QUESTIONS = [
    {"q": "Bestimme Kasus + Funktion: Romam",
     "options": ["Ablativ (Ort: wo?)", "Lokativ (Ort: wo?)", "Akkusativ der Richtung (wohin?)", "Genitiv (Besitz)"],
     "answer": 2,
     "explain": "Städtenamen: Akkusativ ohne Präposition = Richtung → Romam (wohin?)."},
    {"q": "Wähle die korrekte Form: Senatores ___ sedent.",
     "options": ["Romam", "Romae", "Romā (Abl.)", "ad Romam"],
     "answer": 1,
     "explain": "Ort bei Städten = Lokativ → Romae (sie sitzen in Rom)."},
    {"q": "Gladiatores pugnant ___ amphitheatro.",
     "options": ["in (Akk.) – in amphitheatrum", "in (Abl.) – in amphitheatro", "ad amphitheatrum", "ex amphitheatro"],
     "answer": 1,
     "explain": "Ort (wo?) bei Gebäuden → in + Ablativ: in amphitheatro."},
    {"q": "Spectatores veniunt ___ urbe.",
     "options": ["in", "ad", "ex", "cum"],
     "answer": 2,
     "explain": "Herkunft (woher?) → ex + Ablativ: ex urbe."},
    {"q": "Discipuli intrant ___ scholam.",
     "options": ["in", "de", "e/ex", "cum"],
     "answer": 0,
     "explain": "Richtung (wohin?) → in + Akkusativ: in scholam."},
    {"q": "Übersetzung: Ars longa, vita brevis.",
     "options": ["Die Kunst ist lang, das Leben ist kurz.",
                 "Die Kunst ist schwierig, das Leben ist schön.",
                 "Alle Wege führen nach Rom.",
                 "Die Lehrer sind streng, die Schüler sind müde."],
     "answer": 0, "explain": "Klassisches Sprichwort."},
    {"q": "–arum steht für …",
     "options": ["Genitiv Plural (1. Dekl.)", "Akkusativ Singular (1. Dekl.)", "Nom. Pl. (2. Dekl. mask.)", "Dat./Abl. Pl. (2. Dekl.)"],
     "answer": 0, "explain": "-arum = Gen. Pl. 1. Dekl. (puellarum)."},
    {"q": "servis ist …",
     "options": ["Dativ/Ablativ Plural (2. Dekl.)", "Genitiv Singular (2. Dekl.)", "Nom. Plural (1. Dekl.)", "Akk. Singular (3. Dekl.)"],
     "answer": 0, "explain": "servis: Dat./Abl. Pl. (den/mit den Sklaven)."},
    {"q": "Wähle den richtigen Satz für „Ich bin in Rom.“",
     "options": ["Romam sum.", "Romae sum.", "in Romam sum.", "ad Romam sum."],
     "answer": 1, "explain": "Ort bei Städten = Lokativ → Romae sum."},
    {"q": "Wähle den richtigen Satz für „Ich gehe nach Rom.“",
     "options": ["Romae eo.", "in Roma eo.", "Romam eo.", "ex Roma eo."],
     "answer": 2, "explain": "Richtung zur Stadt → Akkusativ ohne Präposition: Romam eo."},
    {"q": "Athenis bedeutet …",
     "options": ["in Athen (Lokativ Pl.)", "nach Athen (Akk.)", "aus Athen (Abl.)", "bei Athen (Dativ)"],
     "answer": 0, "explain": "Athen ist Pluralwort; Athenis = Lokativ Pl. → in Athen."},
    {"q": "Welche Kombination drückt einen Ort (wo?) aus?",
     "options": ["in + Akkusativ", "in + Ablativ", "ad + Akkusativ", "ex + Ablativ"],
     "answer": 1, "explain": "Ort (wo?) bei Gebäuden → in + Ablativ."},
    {"q": "„Omnes viae Romam ducunt“: Funktion von Romam?",
     "options": ["Lokativ (Ort)", "Ablativ (Ort)", "Genitiv (Besitz)", "Akkusativ der Richtung (wohin)"],
     "answer": 3, "explain": "Romam = Akkusativ der Richtung (wohin?)."},
    {"q": "1. Dekl.: Nominativ Plural?",
     "options": ["-ae", "-as", "-arum", "-is"],
     "answer": 0, "explain": "Nom. Pl. 1. Dekl. = -ae (viae)."},
    {"q": "2. Dekl. mask.: Nominativ Plural?",
     "options": ["-i", "-os", "-um", "-is"],
     "answer": 0, "explain": "Nom. Pl. 2. Dekl. mask. = -i (servi)."},
]

CHEATSHEET = """
### Ablativ vs. Lokativ (Ort „wo?“)
- **Ablativ**: mit **in** → *in amphitheatro*, *in schola*. Gilt für Gebäude/Räume/Orte.  
- **Lokativ**: **ohne** Präposition, **nur** bei Städten und wenigen Wörtern wie **domi** → *Romae*, *Athenis*, *domi*.

### Richtung (wohin?)
- **Stadtname**: Akkusativ **ohne** Präposition → *Romam*, *Athenas*.  
- **Gebäude/Raum**: **in + Akkusativ** → *in scholam*, *in amphitheatrum*.

### Herkunft (woher?)
- **ex/e**, **a/ab**, **de** + Ablativ → *ex urbe*, *a Roma*, *de monte*.

### Deklination – Kurzüberblick
**1. Deklination (meist fem.)**  
- Sg.: -a, -ae, -ae, -am, -a  
- Pl.: -ae, -arum, -is, -as, -is  

**2. Deklination (mask./neutr.)**  
- mask. Sg.: -us/-er, -i, -o, -um, -o · Pl.: -i, -orum, -is, -os, -is  
- neutr. Sg.: -um, -i, -o, -um, -o · Pl.: -a, -orum, -is, -a, -is
"""

# ---------------------- Session state ----------------------
def ss_init():
    # Flashcards
    st.session_state.setdefault("card_index", 0)
    st.session_state.setdefault("show_answer", False)
    st.session_state.setdefault("known", 0)
    st.session_state.setdefault("unknown", 0)

    # MC
    if "mc_order" not in st.session_state:
        st.session_state.mc_order = list(range(len(MC_QUESTIONS)))
        random.shuffle(st.session_state.mc_order)
    st.session_state.setdefault("mc_pos", 0)
    st.session_state.setdefault("mc_score", 0)
    st.session_state.setdefault("mc_feedback", "")
    st.session_state.setdefault("finished", False)

    # Arcade game
    g = st.session_state
    g.setdefault("game_running", False)
    g.setdefault("game_lives", 3)
    g.setdefault("game_score", 0)
    g.setdefault("game_combo", 0)
    g.setdefault("game_qidx", 0)
    g.setdefault("game_order", random.sample(range(len(MC_QUESTIONS)), len(MC_QUESTIONS)))
    g.setdefault("game_difficulty", "Mittel")
    g.setdefault("game_deadline", 0.0)
    g.setdefault("game_5050_left", True)
    g.setdefault("game_hidden_opts", [])
    g.setdefault("game_msg", "")

def time_limit_for(diff: str) -> int:
    return {"Leicht": 20, "Mittel": 15, "Schwer": 10}.get(diff, 15)

def set_deadline():
    st.session_state.game_deadline = time.time() + time_limit_for(st.session_state.game_difficulty)

def start_new_game():
    g = st.session_state
    g.game_running = True
    g.game_lives = 3
    g.game_score = 0
    g.game_combo = 0
    g.game_qidx = 0
    g.game_order = random.sample(range(len(MC_QUESTIONS)), len(MC_QUESTIONS))
    g.game_5050_left = True
    g.game_hidden_opts = []
    g.game_msg = ""
    set_deadline()

def save_score(name: str, score: int):
    path = "leaderboard.json"
    data = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append({"name": name, "score": score, "ts": int(time.time())})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_scores():
    path = "leaderboard.json"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# ---------------------- UI ----------------------
ss_init()
tabs = st.tabs(["🃏 Lernkarten", "✅ Multiple-Choice", "🎮 Arcade-Quiz", "📎 Grammatik-Spickkarte"])

# ----- Tab 1: Flashcards (Q+A) -----
with tabs[0]:
    st.subheader("Lernkarten (Q → A)")
    st.write("1) **Antwort zeigen** → 2) optional **Gewusst/Nicht gewusst** klicken → 3) **➡️ Nächste Karte**")

    card = FLASHCARDS[st.session_state.card_index]
    st.markdown(f"**Frage:** {card['q']}")

    # Button-Leiste: Show / Known / Unknown / Next
    c1, c2, c3, c4 = st.columns([1,1,1,1.2])

    if c1.button("Antwort zeigen", key="fc_show", use_container_width=True):
        st.session_state.show_answer = True

    if c2.button("✅ Gewusst", key="fc_known", type="primary", use_container_width=True):
        st.session_state.known += 1

    if c3.button("❌ Nicht gewusst", key="fc_unknown", use_container_width=True):
        st.session_state.unknown += 1

    if c4.button("➡️ Nächste Karte", key="fc_next", use_container_width=True):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(FLASHCARDS)
        st.session_state.show_answer = False
        _rerun()

    if st.session_state.show_answer:
        st.info(f"**Antwort:** {card['a']}")

    total = st.session_state.known + st.session_state.unknown
    ratio = (st.session_state.known / total) if total else 0.0
    st.progress(ratio)
    st.caption(f"Gewusst: {st.session_state.known} · Nicht gewusst: {st.session_state.unknown}")

    if st.button("🔄 Fortschritt zurücksetzen", key="fc_reset"):
        st.session_state.card_index = 0
        st.session_state.show_answer = False
        st.session_state.known = 0
        st.session_state.unknown = 0
        _rerun()

# ----- Tab 2: Multiple-Choice -----
with tabs[1]:
    st.subheader("Multiple-Choice-Quiz")

    if st.session_state.finished:
        st.success(f"Fertig! Score: {st.session_state.mc_score} / {len(MC_QUESTIONS)}")
        if st.button("↩️ Nochmal spielen", key="mc_restart"):
            st.session_state.mc_order = list(range(len(MC_QUESTIONS)))
            random.shuffle(st.session_state.mc_order)
            st.session_state.mc_pos = 0
            st.session_state.mc_score = 0
            st.session_state.mc_feedback = ""
            st.session_state.finished = False
            _rerun()
    else:
        idx = st.session_state.mc_order[st.session_state.mc_pos]
        q = MC_QUESTIONS[idx]
        st.markdown(f"**Frage {st.session_state.mc_pos + 1} von {len(MC_QUESTIONS)}**")
        st.write(q["q"])

        choice = st.radio("Antwort wählen:", q["options"], index=None, label_visibility="collapsed",
                          key=f"mc_radio_{st.session_state.mc_pos}")

        b1, b2 = st.columns(2)
        if b1.button("Antwort prüfen", key=f"mc_check_{st.session_state.mc_pos}", type="primary", disabled=(choice is None)):
            if q["options"].index(choice) == q["answer"]:
                st.session_state.mc_score += 1
                st.session_state.mc_feedback = "✅ Richtig!"
            else:
                correct_text = q["options"][q["answer"]]
                st.session_state.mc_feedback = f"❌ Falsch. Richtig ist: **{correct_text}**"

        if b2.button("Nächste Frage", key=f"mc_next_{st.session_state.mc_pos}"):
            st.session_state.mc_pos += 1
            st.session_state.mc_feedback = ""
            if st.session_state.mc_pos >= len(MC_QUESTIONS):
                st.session_state.finished = True
            _rerun()

        if st.session_state.mc_feedback:
            st.info(st.session_state.mc_feedback)
            st.caption(q["explain"])

        st.caption(f"Aktueller Score: {st.session_state.mc_score}")

# ----- Tab 3: Arcade-Quiz -----
with tabs[2]:
    st.subheader("🎮 Arcade-Quiz")
    g = st.session_state

    if not g.game_running:
        g.game_difficulty = st.radio("Schwierigkeit", ["Leicht", "Mittel", "Schwer"], index=1, horizontal=True, key="arc_diff")
        st.write("Regeln: 3 Leben, Zeitlimit pro Frage, Streak-Multiplikator, 50:50-Joker, Punkte & Bestenliste.")
        c1, c2, _ = st.columns(3)
        if c1.button("▶️ Spiel starten", key="arc_start", type="primary", use_container_width=True):
            start_new_game(); _rerun()
        if c2.button("🔁 Neustart", key="arc_restart", use_container_width=True):
            start_new_game(); _rerun()

    if g.game_running:
        idx = g.game_order[g.game_qidx]
        q = MC_QUESTIONS[idx]

        remaining = max(0, int(g.game_deadline - time.time()))
        hearts = "♥" * g.game_lives + "♡" * (3 - g.game_lives)
        st.markdown(f"**Leben:** {hearts}  |  **Combo:** ×{g.game_combo+1}  |  **Punkte:** {g.game_score}  |  **Restzeit:** {remaining}s")

        colx, coly = st.columns([3,1])
        if coly.button("🪄 50:50", key=f"arc_5050_{g.game_qidx}", disabled=not g.game_5050_left):
            wrong = [i for i in range(len(q["options"])) if i != q["answer"]]
            g.game_hidden_opts = sorted(random.sample(wrong, k=min(2, len(wrong))))
            g.game_5050_left = False
            _rerun()

        shown_opts = [opt for i, opt in enumerate(q["options"]) if i not in g.game_hidden_opts]
        map_to_original = [i for i in range(len(q["options"])) if i not in g.game_hidden_opts]

        st.markdown(f"**Frage {g.game_qidx+1}/{len(MC_QUESTIONS)}**")
        st.write(q["q"])
        choice = st.radio("Antwort:", shown_opts, index=None, label_visibility="collapsed", key=f"arc_radio_{g.game_qidx}")

        b1, b2, b3 = st.columns(3)
        if b1.button("Antwort prüfen", key=f"arc_check_{g.game_qidx}", type="primary", disabled=choice is None):
            if time.time() > g.game_deadline:
                g.game_msg = "⏰ Zeit abgelaufen! −1 Leben."
                g.game_lives -= 1
                g.game_combo = 0
            else:
                chosen_original_index = map_to_original[shown_opts.index(choice)]
                if chosen_original_index == q["answer"]:
                    base, bonus = 100, 5 * remaining
                    mult = g.game_combo + 1
                    gained = base * mult + bonus
                    g.game_score += gained
                    g.game_combo += 1
                    g.game_msg = f"✅ Richtig! +{gained} Punkte (Basis 100 ×{mult} + Zeitbonus {bonus})."
                    st.balloons()
                else:
                    g.game_lives -= 1
                    g.game_combo = 0
                    correct_text = q["options"][q["answer"]]
                    g.game_msg = f"❌ Falsch. Richtig ist: **{correct_text}** (−1 Leben)."
            g.game_qidx += 1
            g.game_hidden_opts = []
            if g.game_qidx >= len(MC_QUESTIONS) or g.game_lives <= 0:
                g.game_running = False
            else:
                set_deadline()
            _rerun()

        if b2.button("⏭️ Überspringen (−1 Leben)", key=f"arc_skip_{g.game_qidx}"):
            g.game_lives -= 1
            g.game_combo = 0
            g.game_qidx += 1
            g.game_hidden_opts = []
            if g.game_qidx >= len(MC_QUESTIONS) or g.game_lives <= 0:
                g.game_running = False
            else:
                set_deadline()
            _rerun()

        if b3.button("🔄 Zeit neu setzen", key=f"arc_reset_time_{g.game_qidx}"):
            set_deadline(); _rerun()

        if g.game_msg:
            st.info(g.game_msg)
            st.caption(q["explain"])

    if not g.game_running and (g.game_qidx > 0):
        st.success(f"Spiel vorbei! Endscore: {st.session_state.game_score}")
        name = st.text_input("Name für die Bestenliste:", value="Max", key="arc_name")
        if st.button("🏁 Score speichern", key="arc_save", type="primary"):
            save_score(name, st.session_state.game_score)
            st.success("Gespeichert!")

    st.subheader("🏆 Bestenliste (Top 10, lokal)")
    board = load_scores()
    if not board:
        st.write("Noch keine Einträge.")
    else:
        for i, row in enumerate(board, start=1):
            st.write(f"{i}. **{row['name']}** — {row['score']} Punkte")

# ----- Tab 4: Cheat Sheet -----
with tabs[3]:
    st.subheader("Grammatik – Ablativ vs. Lokativ & CC de lieu")
    st.markdown(CHEATSHEET)
