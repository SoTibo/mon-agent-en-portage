import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert Droit du Travail", page_icon="⚖️")
st.title("⚖️ Assistant en Droit du Travail")
st.caption("Information juridique basée sur Gemini 1.5 Pro")

# --- SÉCURITÉ : TA CLÉ API ---
# Sur Streamlit, on utilise les "Secrets" pour cacher la clé
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# --- CONFIGURATION DU MODÈLE ---
# Ici, on définit les instructions que tu as créées dans AI Studio
system_instruction = """
TU ES UN EXPERT EN DROIT DU TRAVAIL FRANÇAIS.
[COLLE ICI TES INSTRUCTIONS DEPUIS GOOGLE AI STUDIO]
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction
)

# --- INTERFACE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Posez votre question sur le droit du travail..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Appel à Gemini
        response = model.generate_content(prompt)
        full_response = response.text
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- BAS DE PAGE (LÉGAL) ---
st.sidebar.warning("⚠️ **Avertissement :** Cet agent est un outil d'information. Il ne remplace pas le conseil d'un avocat ou d'un juriste.")
