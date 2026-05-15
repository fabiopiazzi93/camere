import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Hotel Manager Pro - Evento Novembre", layout="wide")

# --- 1. DATABASE COMPLETO HOTEL E CAPACITÀ ---
# Struttura: nome, categoria, posti per tipologia
HOTELS_DB = [
    {"nome": "Hotel De Prati", "cat": "3 stelle_Centro", "singole": 3, "doppie": 4, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Touring", "cat": "3 stelle superior_Centro", "singole": 14, "doppie": 24, "triple": 5, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Carlton", "cat": "3 stelle superior_Centro", "singole": 19, "doppie": 10, "triple": 5, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Astra", "cat": "4 stelle_Centro", "singole": 36, "doppie": 12, "triple": 10, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Europa", "cat": "3 stelle superior_Centro", "singole": 11, "doppie": 13, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Duchessa Isabella", "cat": "4 stelle_Centro", "singole": 5, "doppie": 13, "triple": 3, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Maxxim", "cat": "4 stelle_Centro", "singole": 7, "doppie": 12, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Princess Art", "cat": "4 stelle_Centro", "singole": 5, "doppie": 4, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Locanda Borgonuovo", "cat": "3 stelle_Centro", "singole": 2, "doppie": 2, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Egò Residence", "cat": "3 stelle_Centro", "singole": 10, "doppie": 8, "triple": 7, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Nazionale", "cat": "3 stelle_Centro", "singole": 5, "doppie": 3, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Ferrara", "cat": "4 stelle_Centro", "singole": 28, "doppie": 10, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel The Dome", "cat": "3 stelle_Centro", "singole": 5, "doppie": 4, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Depandance Annunziata", "cat": "4 stelle_Centro", "singole": 3, "doppie": 2, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Lucrezia Borgia", "cat": "3 stelle_Fuori", "singole": 11, "doppie": 11, "triple": 10, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Radisson", "cat": "4 stelle_Fuori", "singole": 31, "doppie": 22, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel B&B", "cat": "3 stelle_Fuori", "singole": 8, "doppie": 8, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Palace INN", "cat": "3 stelle_Fuori", "singole": 38, "doppie": 15, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Duca D'Este", "cat": "4 stelle_Fuori", "singole": 7, "doppie": 10, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Orologio", "cat": "4 stelle_Fuori", "singole": 8, "doppie": 4, "triple": 12, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Principessa Pio", "cat": "3 stelle_Fuori", "singole": 2, "doppie": 2, "triple": 2, "quadruple": 0, "sestuple": 0},
    {"nome": "Hotel Boutique", "cat": "3 stelle_Fuori", "singole": 5, "doppie": 6, "triple": 0, "quadruple": 0, "sestuple": 0},
    {"nome": "Ostello Comune", "cat": "Ostello", "singole": 0, "doppie": 2, "triple": 1, "quadruple": 2, "sestuple": 2},
]

CATEGORIE = sorted(list(set([h['cat'] for h in HOTELS_DB])))

# --- 2. INIZIALIZZAZIONE STATO ---
if 'ospiti' not in st.session_state:
    st.session_state.ospiti = pd.DataFrame(columns=[
        "Codice Scuola", "Nome", "Cognome", "Genere", "Ruolo", "Pacchetto", "Tipo Camera", "VIP", "Hotel Assegnato"
    ])

# --- 3. SIDEBAR NAVIGAZIONE ---
st.sidebar.title("🏨 Menu Gestione")
page = st.sidebar.radio("Seleziona Fase:", ["➕ Inserimento", "🗂️ Database e VIP", "🚀 Ottimizzazione"])

# --- 4. PAGINA: INSERIMENTO ---
if page == "➕ Inserimento":
    st.header("Registrazione Nuovo Ospite")
    with st.form("form_ospite", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            scuola = st.text_input("Codice Scuola (es. SCUOLA01)")
            nome = st.text_input("Nome")
            cognome = st.text_input("Cognome")
            genere = st.selectbox("Genere", ["M", "F"])
        with c2:
            ruolo = st.selectbox("Ruolo", ["Studente", "Docente"])
            pacchetto = st.selectbox("Pacchetto (Categoria)", CATEGORIE)
            
            # Logica dinamica camere
            if pacchetto == "Ostello":
                opzioni_cam = ["doppie", "triple", "quadruple", "sestuple"]
            else:
                opzioni_cam = ["singole", "doppie", "triple"]
            
            camera = st.selectbox("Tipo Camera", opzioni_cam)
            vip = st.checkbox("VIP (Assegnazione fissa)")
            
            hotel_disponibili = [h['nome'] for h in HOTELS_DB if h['cat'] == pacchetto]
            hotel_fisso = st.selectbox("Hotel per VIP", ["-"] + hotel_disponibili)

        if st.form_submit_button("Salva Ospite"):
            nuovo = pd.DataFrame([[scuola, nome, cognome, genere, ruolo, pacchetto, camera, vip, hotel_fisso if vip else "NON ASSEGNATO"]], 
                                 columns=st.session_state.ospiti.columns)
            st.session_state.ospiti = pd.concat([st.session_state.ospiti, nuovo], ignore_index=True)
            st.success("Ospite inserito con successo!")

# --- 5. PAGINA: DATABASE E VIP ---
elif page == "🗂️ Database e VIP":
    st.header("Gestione Dati e Modifiche")
    st.info("Qui puoi modificare i dati o bloccare manualmente una persona in un hotel.")
    
    # Editor interattivo
    edited_df = st.data_editor(st.session_state.ospiti, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Salva modifiche database"):
        st.session_state.ospiti = edited_df
        st.success("Database aggiornato!")

# --- 6. PAGINA: OTTIMIZZAZIONE ---
elif page == "🚀 Ottimizzazione":
    st.header("Algoritmo di Allocazione Intelligente")
    
    if st.button("Avvia Incastro Ottimale"):
        df = st.session_state.ospiti.copy()
        
        # 1. Preparazione Inventario (Posti Letto Reali)
        # Convertiamo i tipi camera in numeri di letti
        mappa_letti = {"singole": 1, "doppie": 2, "triple": 3, "quadruple": 4, "sestuple": 6}
        
        # Reset assegnazioni non VIP
        df.loc[df['VIP'] == False, 'Hotel Assegnato'] = "NON ASSEGNATO"
        
        # Creiamo un inventario di lavoro
        inv_lavoro = {}
        for h in HOTELS_DB:
            inv_lavoro[h['nome']] = {k: h[k] for k in mappa_letti.keys()}
        
        # Sottraiamo i VIP già assegnati
        for _, v in df[df['VIP'] == True].iterrows():
            if v['Hotel Assegnato'] in inv_lavoro:
                inv_lavoro[v['Hotel Assegnato']][v['Tipo Camera']] -= (1 / mappa_letti[v['Tipo Camera']])

        # 2. RAGGRUPPAMENTO PER SCUOLA (Priorità compattezza)
        # Ordiniamo le scuole per numero di membri (le più grandi prima)
        scuole_order = df[df['VIP'] == False]['Codice Scuola'].value_counts().index
        
        for cod_scuola in scuole_order:
            # Per ogni scuola, dividiamo per pacchetto/genere/camera (vincoli tecnici)
            gruppi = df[(df['Codice Scuola'] == cod_scuola) & (df['VIP'] == False)].groupby(['Pacchetto', 'Genere', 'Ruolo', 'Tipo Camera'])
            
            for (pacc, gen, ruolo, t_cam), data in gruppi:
                posti_necessari = len(data)
                camere_necessarie = math.ceil(posti_necessari / mappa_letti[t_cam])
                
                # Cerchiamo un hotel in quel pacchetto che abbia le camere
                hotel_scelto = "NON ASSEGNATO"
                for h_nome, h_data in inv_lavoro.items():
                    # Verifichiamo se l'hotel appartiene al pacchetto corretto
                    h_info = next(item for item in HOTELS_DB if item["nome"] == h_nome)
                    if h_info['cat'] == pacc and h_data[t_cam] >= (posti_necessari / mappa_letti[t_cam]):
                        hotel_scelto = h_nome
                        # Aggiorniamo inventario (contando i letti reali occupati)
                        inv_lavoro[h_nome][t_cam] -= (posti_necessari / mappa_letti[t_cam])
                        break
                
                df.loc[data.index, 'Hotel Assegnato'] = hotel_scelto

        st.session_state.ospiti = df
        st.success("Ottimizzazione completata!")

    # Visualizzazione Risultati
    st.subheader("Rooming List Finale")
    hotel_filter = st.selectbox("Filtra per Hotel:", ["Tutti"] + [h['nome'] for h in HOTELS_DB])
    
    view_df = st.session_state.ospiti
    if hotel_filter != "Tutti":
        view_df = view_df[view_df['Hotel Assegnato'] == hotel_filter]
    
    st.dataframe(view_df.sort_values(["Hotel Assegnato", "Codice Scuola"]), use_container_width=True)

    # Conteggio di controllo
    st.sidebar.subheader("Statistiche")
    assegnati = len(st.session_state.ospiti[st.session_state.ospiti['Hotel Assegnato'] != "NON ASSEGNATO"])
    st.sidebar.write(f"Assegnati: {assegnati} / {len(st.session_state.ospiti)}")