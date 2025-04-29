import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Portefeuille Beheer", layout="centered")

st.title("💼 Aandelen Portefeuille Beheer")

# Sessie-opslag voor portefeuille
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Aandeel", "Aantal", "Aankoopprijs", "Huidige prijs", "Winst/Verlies"])

# Invoervelden voor nieuwe transactie
st.subheader("📈 Voeg een transactie toe")
aandeel = st.text_input("Aandeel Ticker (bijv. AAPL)", "")
aantal = st.number_input("Aantal Aandelen", min_value=1, step=1)
aankoopprijs = st.number_input("Aankoopprijs per aandeel ($)", min_value=0.0, step=0.01)

if st.button("Voeg Transactie Toe"):
    if aandeel and aantal > 0 and aankoopprijs > 0:
        try:
            # Haal de actuele prijs op via yfinance
            ticker = yf.Ticker(aandeel)
            huidig_data = ticker.history(period="1d")
            huidig_prijs = huidig_data["Close"].iloc[-1]

            winst_verlies = (huidig_prijs - aankoopprijs) * aantal

            # Voeg de transactie toe aan de portefeuille
            nieuwe_transactie = pd.DataFrame([{
                "Aandeel": aandeel,
                "Aantal": aantal,
                "Aankoopprijs": aankoopprijs,
                "Huidige prijs": huidig_prijs,
                "Winst/Verlies": winst_verlies
            }])

            st.session_state.portfolio = pd.concat([st.session_state.portfolio, nieuwe_transactie], ignore_index=True)

            st.success(f"Transactie toegevoegd! {aandeel} | {aantal} aandelen gekocht tegen ${aankoopprijs:.2f} per stuk.")

        except Exception as e:
            st.error(f"Er is iets mis gegaan: {e}")
    
    else:
        st.error("Zorg ervoor dat alle velden correct zijn ingevuld!")

# Weergave van portefeuille
st.subheader("📊 Je Portefeuille")
if not st.session_state.portfolio.empty:
    st.dataframe(st.session_state.portfolio)
    totaal_winst_verlies = st.session_state.portfolio["Winst/Verlies"].sum()
    st.metric("Totale Winst/Verlies", f"${totaal_winst_verlies:.2f}")
else:
    st.warning("Je hebt nog geen aandelen toegevoegd!")
