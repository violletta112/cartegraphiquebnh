import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Emplacement Agences",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display the image
st.markdown(
    "<div style='text-align: center;'>"
    "<img src='https://bnh.dz/img/logo13.png' width='900'/>"
    "</div>",
    unsafe_allow_html=True
)
st.title("Déploiement des agences de BNH")

options = ['Choisir une année', '2024', '2025', '2026']
optionn = ['Aucun choix', 'Avec directeur', 'Sans directeur']
WILAYAS = ['choisir une wilaya', 'ALGER', 'CONSTANTINE', 'ORAN', 'BISKRA', 'SÉTIF', 'CHLEF','BECHAR']

# Create a Folium map
m = folium.Map([35.7950980697429, 3.1787263226179263], zoom_start=6)

col1, col2 = st.columns([3, 2])

with col1:
    # Allow wilaya selection first
    choisir = st.selectbox('Choisir une wilaya', WILAYAS, key='wilaya_choice')

    if choisir != 'choisir une wilaya':
        # Display message based on selected wilaya
        messages = {
            'ALGER': "La wilaya d'Alger contient deux agences : <span style='color:red;'><strong>Bab Ezzouar</strong></span> et <span style='color:red;'><strong>El Achour</strong></span>.",
            'CONSTANTINE': "Charger le fichies de Constantine.",
            'ORAN': "Charger le fichies d'Oran.",
            'BISKRA': "Charger le fichies de Biskra.",
            'SÉTIF': "Charger le fichies de Sétif.",
            'CHLEF': "Charger le fichies de Chlef.",
            'BECHAR': "Charger le fichies de Bechar."
        }
        st.markdown(messages.get(choisir, ""), unsafe_allow_html=True)

        # File uploader for Excel file
        uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"])

        if uploaded_file is not None:
            df_uploaded = pd.read_excel(uploaded_file)
            st.write(df_uploaded)

            # Process uploaded file and display results
            try:
                total1 = df_uploaded.iloc[:6, 2].sum()
                total2 = df_uploaded.iloc[6:, 2].sum()
                total_ht = df_uploaded.iloc[:, 1].sum()

                st.write(f"Le taux D'AMENAGEMENTS total est : {total1:.4f}")
                st.write(f"Le taux EQUIPEMENTS total est : {total2:.4f}")
                total_total = total1 + total2
                st.write(f"Le taux total est : {total_total:.4f}")
                st.write(f"Le total des MONTANT HT est : {total_ht:.4f}")
            except Exception as e:
                st.error(f"Erreur lors du chargement des données pour la wilaya : {e}")

    # Year and options selection can still be included below if needed
    choice = st.selectbox('Sélectionner une année pour voir les agences existantes', options)
    
    if choice != 'Choisir une année':
        try:
            if choice == '2024':
                df = pd.read_excel('carte.graphique.xlsx')
            elif choice == '2025':
                df = pd.read_excel('carte.graphique2.xlsx')
            else:
                df = pd.read_excel('carte.graphique3.xlsx')

            # Clean column names
            df.columns = df.columns.str.strip()

            # Add markers to the Folium map based on year selection
            for index, row in df.iterrows():
                folium.CircleMarker([row['latitude'], row['longitude']],
                                    radius=10,
                                    color='yellow',
                                    fill=True,
                                    fill_color='red').add_to(m)
                folium.Marker([row['latitude'], row['longitude']],
                              popup=f"<b>Emplacement:</b> {row['name']}, <br><b>Latitude:</b> {row['latitude']}, <br><b>Longitude:</b> {row['longitude']}").add_to(m)

        except FileNotFoundError as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
        except KeyError as e:
            st.error(f"Erreur : La colonne {e} n'existe pas dans le DataFrame.")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

with col2:
    # Display the map with Streamlit-Folium
    st_folium(m, width=600, height=300)
