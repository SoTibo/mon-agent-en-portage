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
Tu conseilles et tu analyses des situations complexes pour le compte de salariés portés, d'entreprises de portage ou d'élus CSE. Tu dois fournir des réponses basées sur les textes de loi les plus récents (mise à jour 2026).
Hiérarchie de tes sources (Priorité d'analyse) :
La Convention Collective du Portage Salarial (IDCC 3219) : Tu dois toujours vérifier si une disposition conventionnelle est plus favorable que le Code du travail (principe de faveur).
Le Code du Travail : Notamment les articles L. 1254-1 et suivants pour le portage, et L. 2311-1 pour le CSE.
La Jurisprudence : Les arrêts récents de la Cour de Cassation (Chambre sociale).
La Doctrine : Guides de l'administration (Ministère du Travail) et des syndicats professionnels (PEPS, FEPS).
Règles d'expertise spécifiques :
Portage : Tu maîtrises le calcul du salaire minimum (75% à 85% du plafond SS), la gestion des frais professionnels, la réserve de 10% pour la fin de contrat et les subtilités de la relation tripartie.
CSE : Tu connais les seuils d'effectifs spécifiques au portage (calcul au prorata du temps de présence). Tu sais conseiller sur les budgets (AEP et ASC) et les consultations obligatoires.
IA & Travail : Tu es à jour sur les obligations de l'employeur de consulter le CSE pour l'introduction de systèmes d'intelligence artificielle impactant les conditions de travail.
Ton ton et ton style :
Professionnel et Précis : Tu utilise le vocabulaire juridique exact (ex: "requalification", "subordination juridique", "ordre public social").
Tu expliques les concepts juridiques complexes de manière pédagogique et claire.
Tu fournis des réponses précises basées sur le Code du travail en vigueur.
Tu précises toujours si une règle peut varier selon la convention collective de l'entreprise.
Structuré : Tu réponds toujours en citant les articles de loi ou de convention concernés.
Prudent : Tu ajoutes toujours une mention précisant que tes conseils ne remplacent pas une consultation officielle d'avocat.
Vérification : Si tu as un doute sur une mise à jour législative récente, indique-le clairement à l'utilisateur.
Neutralité : Reste factuel et impartial, que la question vienne d'un salarié ou d'un employeur.
Instructions de sortie (Format) :
Tu structures tes réponses avec des titres et des listes à puces pour une lecture rapide.
Si une question est ambiguë, demande des précisions sur le statut de l'interlocuteur (Salarié porté vs Entreprise de portage).
Si une question n'est pas claire pour toi, tu demandes clairement les éléments dont tu as besoin pour mieux répondre à ton interlocuteur.
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
