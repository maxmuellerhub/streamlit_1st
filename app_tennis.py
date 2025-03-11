import streamlit as st
import pandas as pd
import os
import time
import utils.ftp_aw as aw_ftp

ftp_server = st.secrets["STOR_URL"]
username = st.secrets["STOR_USERNAME"]
password = st.secrets["STOR_PW"]
directory = '/'

st.set_page_config(
    page_title="Tenniskalender",
    layout="centered",
)

# st.title(":tennis: Tenniskalender :tennis:")

####  Functions  ####
def store_value(source, destination):
    st.session.state[destination] = st.session.state[source]

####  Variablen   ###
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'username' not in st.session_state: 
    st.session_state.username = "Unbekannt"
if 'file_from_server' not in st.session_state: 
    st.session_state.file_from_server = ""          # letzter Stand von ftp, der am Anfang der Session geladen wird

spieler = ["simone", "micha", "ute", "birgit", "margret", "heidi", ]

def main_app():

    def read_kalender():
        if st.session_state.file_from_server=="" and True:         # bei Session Start: lokalen "tenniscalender.csv" mit letztem von Server aktualisieren
            print("Trying to get Server Data")
            last_file = aw_ftp.get_last_file(ftp_server, username, password, directory)
            if last_file.endswith(".csv") :
                print(last_file)
                st.session_state.file_from_server=last_file
                timestr=time.strftime("_%Y%m%d-%H%M%S")     
                os.rename("tenniskalender.csv", "tenniskalender"+timestr+".csv")
                os.rename(last_file, "tenniskalender.csv")
        df = pd.read_csv("tenniskalender.csv")
        return df.iloc[:, [1, 2, 3, 4, 5, 6, 7]]

    dfall = read_kalender()

    def ini_kalender():
        termine = ["01.10.24", "08.10.24", "15.10.24", "22.10.24", "29.10.24", "05.11.24", 
                "12.11.24", "19.11.24", "26.11.24", "03.12.24", "10.12.24", "17.12.24", 
                "07.01.25", "14.01.25", "21.01.25", "28.01.25", "04.02.25", "11.02.25",
                "18.02.25", "25.02.25", "04.03.25", "11.03.25", "18.03.25", "25.03.25", 
                "01.04.25", "08.04.25", "15.04.25", "22.04.25"           
                ]
        anzahl_termine = len(termine)

        spieler1 = {"termin": termine, 
                    "Simone": [False for i in range(anzahl_termine)] }
        df1 = pd.DataFrame(spieler1)

        spieler2 = {"termin": termine, 
                    "Micha": [False for i in range(anzahl_termine)] }
        dfall = df1.set_index('termin').join(pd.DataFrame(spieler2).set_index('termin') )

        spieler3 = {"termin": termine, 
                    "Ute": [False for i in range(anzahl_termine)] }
        dfall = dfall.join(pd.DataFrame(spieler3).set_index('termin') )

        spieler3 = {"termin": termine, 
                    "Birgit": [False for i in range(anzahl_termine)] }
        dfall = dfall.join(pd.DataFrame(spieler3).set_index('termin') )

        spieler4 = {"termin": termine, 
                    "Margret": [False for i in range(anzahl_termine)] }
        dfall = dfall.join(pd.DataFrame(spieler4).set_index('termin') )

        spieler5 = {"termin": termine, 
                    "Heidi": [False for i in range(anzahl_termine)] }
        dfall = dfall.join(pd.DataFrame(spieler5).set_index('termin') )
        return dfall

    # "akt. Session State: ", st.session_state

    col1, col2 = st.columns([3,1])

    col1.write(f"<p style='font-size:24px; color:yellow'>🎾 Spielplan Da LL2 🎾      für {st.session_state.username}</p>", unsafe_allow_html=True)

    config = {
        'termin' : st.column_config.TextColumn('Termin'),
        'Micha' : st.column_config.CheckboxColumn('Mi'),
        'Ute' : st.column_config.CheckboxColumn('U' ),
        'Birgit' : st.column_config.CheckboxColumn('B'),
        'Margret' : st.column_config.CheckboxColumn('Ma'),
        'Heidi' : st.column_config.CheckboxColumn('H'),
        'Simone' : st.column_config.CheckboxColumn('Simone'),
    }

    edited_df = st.data_editor(dfall, 
                            height = 600,
                            use_container_width = False, 
                            hide_index = True,
                            disabled=["termin"],    # ["termin", "Simone", "Micha", "Ute", "Birgit", "Margret", "Heidi"],
                            key="datatable", 
                            )             # column_config=config
    
    if col2.button("Speichern"):
        with st.spinner(text = "Speichere die Daten"):
            edited_df.to_csv("tenniskalender.csv")
            timestr = time.strftime("_%Y%m%d-%H%M%S")                   # ohne Angabe Zeitzone wird wohl Server-Zeitzone verwendet
            user = st.session_state.username
            filename = "tenniskalender_"+user+timestr+".csv"
            edited_df.to_csv(filename)
            aw_ftp.upload_file(ftp_server, username, password, filename, directory='/')
            st.success("Termine gespeichert")

    if st.session_state.username=="margret":
        st.write(f"letztes File vom Server: {st.session_state.file_from_server}")
        st.write('gespeicherte Tabellen:')
        filenames = [f for f in os.listdir('.') if f.endswith('.csv')]
        st.write(filenames) 

    # /end main_app()


# "akt. Session State: ", st.session_state



if  not st.session_state.logged_in:
    with st.form(key="login", clear_on_submit=False):
        username = st.text_input('Bitte Name eintragen und 2 x Submit drücken.')
        # password = st.text_input('Password')
        if st.form_submit_button('Submit') and username.lower().strip() in spieler:
            st.session_state.logged_in=True
            st.session_state.username=username.lower().strip()
else:
    main_app()