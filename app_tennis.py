import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(
    page_title="Tenniskalender",
    layout="wide",
)

spieler = ["simone", "micha", "ute", "birgit", "margret", "heidi", ]


def main_app():
    # @st.cache_data
    def read_kalender():
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

    col1, col2 = st.columns([1,1])
    col1.write(":tennis: Tenniskalender :tennis:")

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
            timestr = time.strftime("_%Y%m%d-%H%M%S")  
            edited_df.to_csv("tenniskalender"+timestr+".csv")
            st.success("Termine gespeichert")
    # /end main_app()


if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'username' not in st.session_state: 
    st.session_state.username = "Unbekannt"

# "akt. Session State: ", st.session_state

if  not st.session_state.logged_in:
    with st.form(key="login", clear_on_submit=False):
        username = st.text_input('Bitte Name eintragen und 2 x Submit drücken.', key = 'username')
        # password = st.text_input('Password')
        if st.form_submit_button('Submit') and username.lower().strip() in spieler:
            st.session_state.logged_in=True
else:
    main_app()