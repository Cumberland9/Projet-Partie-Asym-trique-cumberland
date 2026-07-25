import streamlit as st
import rsa

st.title("Projet Cryptographie Asymétrique et MITM")
st.write("Simulation d'un échange sécurisé entre Alice et Bob, avec une tentative d'attaque par Eve.")

# Génération des clés en arrière-plan (stockées dans la session pour ne pas les recréer à chaque clic)
if 'alice_pub' not in st.session_state:
    st.session_state.alice_pub, st.session_state.alice_priv = rsa.newkeys(512)
    st.session_state.bob_pub, st.session_state.bob_priv = rsa.newkeys(512)

st.sidebar.header("Configuration des acteurs")
st.sidebar.write("- **Alice** : Expéditeur")
st.sidebar.write("- **Bob** : Destinataire")
st.sidebar.write("- **Eve** : Attaquant (MITM)")

# Saisie du message par Alice
st.subheader("1. Envoi du message par Alice")
message_alice = st.text_input("Message secret d'Alice pour Bob :", "Bonjour Bob, c'est un secret.")

if st.button("Lancer la simulation de transmission"):
    if message_alice == "":
        st.warning("Écris un message d'abord !")
    else:
        # Chiffrement par Alice avec la clé publique de Bob
        msg_chiffre = rsa.encrypt(message_alice.encode('utf-8'), st.session_state.bob_pub)
        
        st.success("Message chiffré avec la clé publique de Bob et envoyé sur le réseau.")
        st.code(msg_chiffre)

        # --- SCENARIO EVE (MITM) ---
        st.subheader("2. Interception par Eve (Homme du Milieu)")
        st.write("Eve intercepte le message chiffré sur le réseau...")
        
        # Eve essaie de le lire
        try:
            # Eve essaie de décoder avec sa propre clé ou sans la bonne clé privée
            tentative_lecture = rsa.decrypt(msg_chiffre, st.session_state.alice_priv).decode('utf-8')
        except:
            tentative_lecture = "[ÉCHEC] Impossible de déchiffrer ! Eve ne possède pas la clé privée de Bob."

        st.info(f"**Ce qu'Eve voit / lit :** {tentative_lecture}")

        # Eve essaie de modifier le message
        st.write("Eve essaie de modifier le message chiffré en route...")
        msg_modifie = msg_chiffre + b"corruption"

        # --- RECEPTION PAR BOB ---
        st.subheader("3. Réception par Bob")
        
        # Bob essaie de déchiffrer le message modifié par Eve
        try:
            message_final = rsa.decrypt(msg_modifie, st.session_state.bob_priv).decode('utf-8')
            st.write(f"Bob a reçu : {message_final}")
        except rsa.DecryptionError:
            st.error("[ERREUR DECHIFFREMENT] Bob signale que le message a été corrompu ou modifié en transit par Eve !")
            st.write("-> **Conclusion** : Eve ne peut pas lire le message secret, et si elle le modifie, Bob s'en aperçoit immédiatement.")
