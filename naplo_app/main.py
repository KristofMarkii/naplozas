import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import uuid  # Egyedi azonosítók generálásához

# Alapértelmezett téma beállítás (sötét)
st.set_page_config(page_title="Napi Naplózó", page_icon="📓", layout="wide")

# CSS a sötét téma és egyéb stílusok beállításához
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    .stButton.red>button {
        background-color: #FF5252;
        color: white;
    }
    .stButton.green>button {
        background-color: #4CAF50;
        color: white;
    }
    .big-green-button>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 15px 32px;
        width: 100%;
    }
    .header-text {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .container {
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .task-item {
        background-color: #383838;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
    }
    .book-symbol {
        font-size: 50px;
        text-align: center;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Egyedi ID generálása
def generate_unique_id():
    return str(uuid.uuid4())  # UUID használata a még jobb egyediség érdekében

# Adatok betöltése fájlból
def load_data():
    try:
        if os.path.exists("naplo_adatok.json"):
            with open("naplo_adatok.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Ellenőrizzük és betöltjük az adatokat
                if "tasks" in data:
                    st.session_state.tasks = data["tasks"]
                else:
                    st.session_state.tasks = {}
                    
                if "activities" in data:
                    st.session_state.activities = data["activities"]
                else:
                    st.session_state.activities = {}
                    
                if "ratings" in data:
                    st.session_state.ratings = data["ratings"]
                else:
                    st.session_state.ratings = {}
                    
                if "reading" in data:
                    st.session_state.reading = data["reading"]
                else:
                    st.session_state.reading = {}
                    
                if "activity_list" in data:
                    st.session_state.activity_list = data["activity_list"]
                else:
                    st.session_state.activity_list = ["Példa tevékenység"]
    except Exception as e:
        st.error(f"Hiba történt az adatok betöltésekor: {e}")
        # Alapértelmezett értékek beállítása hiba esetén
        if 'tasks' not in st.session_state:
            st.session_state.tasks = {}
        if 'activities' not in st.session_state:
            st.session_state.activities = {}
        if 'ratings' not in st.session_state:
            st.session_state.ratings = {}
        if 'reading' not in st.session_state:
            st.session_state.reading = {}
        if 'activity_list' not in st.session_state:
            st.session_state.activity_list = ["Példa tevékenység"]

# Adatok mentése fájlba
def save_data():
    try:
        data = {
            "tasks": st.session_state.tasks,
            "activities": st.session_state.activities,
            "ratings": st.session_state.ratings,
            "reading": st.session_state.reading,
            "activity_list": st.session_state.activity_list
        }
        with open("naplo_adatok.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Mentés után újratöltjük az adatokat, hogy biztosítsuk a konzisztenciát
        # load_data()
        return True
    except Exception as e:
        st.error(f"Hiba történt az adatok mentésekor: {e}")
        return False

# Inicializálás és alapértelmezett értékek
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.date.today()
if 'tasks' not in st.session_state:
    st.session_state.tasks = {}
if 'activities' not in st.session_state:
    st.session_state.activities = {}
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}
if 'reading' not in st.session_state:
    st.session_state.reading = {}
if 'activity_list' not in st.session_state:
    st.session_state.activity_list = ["Példa tevékenység"]

# Adatok betöltése
load_data()

# Dátum formázása
def format_date(date):
    return date.strftime("%Y.%m.%d")

def format_date_key(date):
    return date.strftime("%Y-%m-%d")

# Aktuális napi kulcs
current_date_key = format_date_key(st.session_state.current_date)

# Nap betöltése
def load_day(date_key):
    # Alapértelmezett értékek inicializálása
    if date_key not in st.session_state.tasks:
        st.session_state.tasks[date_key] = []
    if date_key not in st.session_state.activities:
        st.session_state.activities[date_key] = {}
    # Inicializáljuk az összes tevékenységet False-ra
    for activity in st.session_state.activity_list:
        if activity not in st.session_state.activities[date_key]:
            st.session_state.activities[date_key][activity] = False
    if date_key not in st.session_state.ratings:
        st.session_state.ratings[date_key] = 5
    if date_key not in st.session_state.reading:
        st.session_state.reading[date_key] = {"cim": "", "oldalak": 0}

# Az aktuális nap betöltése
load_day(current_date_key)

# Fejléc
st.markdown(f"<h1 class='header-text'>{format_date(st.session_state.current_date)} NAPLÓZÁS</h1>", unsafe_allow_html=True)

# Navigációs gombok
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("◀ Előző nap", key="prev_day", help="Előző napra lépés"):
        st.session_state.current_date -= datetime.timedelta(days=1)
        current_date_key = format_date_key(st.session_state.current_date)
        load_day(current_date_key)
        st.rerun()
with col3:
    if st.button("Következő nap ▶", key="next_day", help="Következő napra lépés"):
        st.session_state.current_date += datetime.timedelta(days=1)
        current_date_key = format_date_key(st.session_state.current_date)
        load_day(current_date_key)
        st.rerun()

# Főtartalom
st.markdown("<div class='container'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

# Bal oldali oszlop: Tevékenységek, olvasott könyv, napi értékelés
with col1:
    st.markdown("<div class='section-header'>Napi Tevékenységek</div>", unsafe_allow_html=True)
    
    # Új tevékenység hozzáadása
    col_a1, col_a2 = st.columns([3, 1])
    with col_a1:
        new_activity = st.text_input("Új tevékenység", key="new_activity_input")
    with col_a2:
        if st.button("Hozzáad", key="add_activity_btn"):
            if new_activity.strip() and new_activity not in st.session_state.activity_list:
                st.session_state.activity_list.append(new_activity)
                # Minden naphoz hozzáadjuk az új tevékenységet False értékkel
                for day_key in st.session_state.activities:
                    st.session_state.activities[day_key][new_activity] = False
                # Azonnal mentjük az adatokat
                save_data()
                st.rerun()
    
    # Tevékenységek checkboxok
    if st.session_state.activity_list:
        for i, activity in enumerate(st.session_state.activity_list):
            # Biztosítjuk, hogy minden tevékenység létezik az adott napon
            if activity not in st.session_state.activities[current_date_key]:
                st.session_state.activities[current_date_key][activity] = False
                
            # Checkbox megjelenítése
            value = st.session_state.activities[current_date_key].get(activity, False)
            checkbox_key = f"activity_{i}_{current_date_key}"
            is_checked = st.checkbox(activity, value=value, key=checkbox_key)
            st.session_state.activities[current_date_key][activity] = is_checked
            
            # Tevékenység törlése gomb
            delete_key = f"delete_activity_{i}_{current_date_key}"
            if st.button("🗑️", key=delete_key):
                if activity in st.session_state.activity_list:
                    st.session_state.activity_list.remove(activity)
                    # Töröljük a tevékenységet minden napból
                    for day_key in st.session_state.activities:
                        if activity in st.session_state.activities[day_key]:
                            del st.session_state.activities[day_key][activity]
                    # Azonnal mentjük az adatokat
                    save_data()
                    st.rerun()
    else:
        st.info("Nincs tevékenység. Adj hozzá újat!")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Olvasott könyv rész
    st.markdown("<div class='section-header'>Olvasott Könyv</div>", unsafe_allow_html=True)
    col_book1, col_book2 = st.columns([1, 2])
    
    with col_book1:
        st.markdown("<div class='book-symbol'>📚</div>", unsafe_allow_html=True)
    
    with col_book2:
        st.session_state.reading[current_date_key]["cim"] = st.text_input(
            "Cím", 
            value=st.session_state.reading[current_date_key].get("cim", ""),
            key=f"book_title_{current_date_key}"
        )
        st.session_state.reading[current_date_key]["oldalak"] = st.number_input(
            "Oldalak száma", 
            min_value=0, 
            value=st.session_state.reading[current_date_key].get("oldalak", 0),
            key=f"book_pages_{current_date_key}"
        )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Napi értékelés
    st.markdown("<div class='section-header'>Napi Értékelés</div>", unsafe_allow_html=True)
    st.session_state.ratings[current_date_key] = st.slider(
        "Értékeld a napodat (1-10):", 
        min_value=1, 
        max_value=10, 
        value=st.session_state.ratings[current_date_key],
        key=f"day_rating_{current_date_key}"
    )
    
    # Értékelési skála ikonsávja
    emojis = ["😢", "😟", "😐", "🙂", "😊", "😃", "😄", "😁", "🌟", "🤩"]
    emoji_index = st.session_state.ratings[current_date_key] - 1
    st.markdown(f"<h3 style='text-align: center'>{emojis[emoji_index]}</h3>", unsafe_allow_html=True)

# Jobb oldali oszlop: Napi teendők és grafikonok
with col2:
    st.markdown("<div class='section-header'>Napi Teendők</div>", unsafe_allow_html=True)
    
    # Új teendő hozzáadása
    col_task1, col_task2 = st.columns([3, 1])
    
    with col_task1:
        new_task = st.text_input("Új teendő", key=f"new_task_input_{current_date_key}")
    
    with col_task2:
        if st.button("Hozzáadás", key=f"add_task_btn_{current_date_key}"):
            if new_task.strip():
                # Egyedi ID generálása az új teendőhöz
                task_id = generate_unique_id()
                
                # Inicializáljuk a tasks[current_date_key] listát, ha még nem létezik
                if current_date_key not in st.session_state.tasks:
                    st.session_state.tasks[current_date_key] = []
                
                # Hozzáadás
                st.session_state.tasks[current_date_key].append({
                    "id": task_id,
                    "text": new_task,
                    "completed": False,
                    "timestamp": datetime.datetime.now().strftime("%H:%M")
                })
                
                # Azonnal mentjük az adatokat
                save_data()
                st.rerun()
    
    # Teendők listája
    if current_date_key in st.session_state.tasks and st.session_state.tasks[current_date_key]:
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        
        # Létrehozunk egy ideiglenes listát a törlésekhez
        tasks_to_keep = []
        
        for i, task in enumerate(st.session_state.tasks[current_date_key]):
            # Biztosítjuk, hogy minden feladatnak van egyedi ID-ja
            if "id" not in task:
                task["id"] = generate_unique_id()
            
            task_id = task["id"]
            col_check, col_text, col_delete = st.columns([1, 5, 1])
            
            with col_check:
                completed = st.checkbox(
                    "", 
                    value=task["completed"], 
                    key=f"task_check_{task_id}_{current_date_key}"
                )
                task["completed"] = completed
            
            with col_text:
                if task["completed"]:
                    st.markdown(f"<del>{task['text']}</del> <small>({task['timestamp']})</small>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{task['text']} <small>({task['timestamp']})</small>", unsafe_allow_html=True)
            
            with col_delete:
                if st.button("🗑️", key=f"delete_task_{task_id}_{current_date_key}"):
                    continue  # Ha törölni kell, ne adjuk hozzá a megtartandó listához
            
            # Ha nem töröljük, adjuk hozzá a megtartandó listához
            tasks_to_keep.append(task)
        
        # Ha változott a lista mérete (törlés történt), frissítsük
        if len(tasks_to_keep) < len(st.session_state.tasks[current_date_key]):
            st.session_state.tasks[current_date_key] = tasks_to_keep
            # Azonnal mentjük az adatokat
            save_data()
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Nincs teendő erre a napra.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Grafikonok
    st.markdown("<div class='section-header'>Statisztikák</div>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Kördiagram a napi értékelésekről
        last_7_days = []
        today = st.session_state.current_date
        
        for i in range(7):
            day = today - datetime.timedelta(days=i)
            day_key = format_date_key(day)
            if day_key in st.session_state.ratings:
                last_7_days.append({
                    "dátum": format_date(day),
                    "értékelés": st.session_state.ratings[day_key]
                })
        
        if last_7_days:
            df_ratings = pd.DataFrame(last_7_days)
            fig_pie = px.pie(
                df_ratings, 
                values="értékelés", 
                names="dátum", 
                title="Napi értékelések eloszlása",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Nincs elegendő adat a kördiagram megjelenítéséhez.")
    
    with col_chart2:
        # Oszlopdiagram a napi aktivitásokhoz
        active_days = []
        
        for i in range(7):
            day = today - datetime.timedelta(days=i)
            day_key = format_date_key(day)
            if day_key in st.session_state.activities:
                active_count = sum(1 for v in st.session_state.activities[day_key].values() if v)
                active_days.append({
                    "dátum": format_date(day),
                    "aktivitások": active_count
                })
        
        if active_days:
            df_activities = pd.DataFrame(active_days)
            fig_bar = px.bar(
                df_activities, 
                x="dátum", 
                y="aktivitások", 
                title="Napi aktivitások",
                color_discrete_sequence=['#4CAF50']
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Nincs elegendő adat az oszlopdiagram megjelenítéséhez.")

st.markdown("</div>", unsafe_allow_html=True)

# Mentés gomb
col_save1, col_save2, col_save3 = st.columns([1, 2, 1])
with col_save2:
    st.markdown("<div class='big-green-button'>", unsafe_allow_html=True)
    if st.button("NAP MENTÉSE", key=f"save_button_{current_date_key}"):
        if save_data():
            st.success("A napi adatok sikeresen elmentve!")
            # Újratöltjük az adatokat a mentés után
            load_data()
        else:
            st.error("Hiba történt a mentés során!")
    st.markdown("</div>", unsafe_allow_html=True)