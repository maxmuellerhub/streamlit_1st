import streamlit as st
import pandas as pd

st.write("Tennisplaner")

@st.cache_data
def read_kalender():
    df = pd.read_csv("./tenniskalender.csv")
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

tab1, tab2 = st.tabs(["", ""])
tab1.write("Tenniskalender")
# tab2.write("this is tab 2")

edited_df = st.data_editor(dfall, use_container_width = True, 
                           hide_index = True,)
if tab2.button("Speichern"):
    edited_df.to_csv("./tenniskalender.csv")


# favorite_Termin = 12.11.24[edited_df["rating"].idxmax()]["Termin"]
