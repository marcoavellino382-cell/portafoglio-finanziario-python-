import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Configurazione della pagina (Titolo e Favicon nella scheda del browser)
st.set_page_config(
    page_title="Portfolio Manager", 
    page_icon="logo.png",  
    layout="wide"
)
# Aggiunge il logo in alto a sinistra sopra il menu laterale di navigazione
st.logo("logo.png")

# 2. Creazione del Menu Laterale di navigazione
st.sidebar.title("Portfolio Manager")
sezione = st.sidebar.radio("Vai alla pagina:", ["1. Titoli e Grafici", "2. Notizie di Mercato", "3. Simulatore Investimenti"])

# ====================================================
# PAGINA 1: TITOLI FINANZIARI E GRAFICI
# ====================================================
if sezione == "1. Titoli e Grafici":
    st.title("📊 Analisi Titoli e Grafici Interattivi")
    st.write("Inserisci il codice di un titolo azionario o crypto per visualizzare i dati in tempo reale.")
    
    # Input per il ticker (es. AAPL per Apple, TSLA per Tesla, BTC-USD per Bitcoin)
    ticker = st.text_input("Inserisci il codice Ticker del titolo (es. AAPL, TSLA, BTC-USD):", "AAPL").upper()
    periodo = st.selectbox("Seleziona l'orizzonte temporale del grafico:", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
    
    if ticker:
        with st.spinner("Scaricamento dati in corso..."):
            try:
                # Scarica i dati storici da Yahoo Finance
                dati_titolo = yf.Ticker(ticker)
                df = dati_titolo.history(period=periodo)
                
                if not df.empty and len(df) > 1:
                    # Calcolo delle metriche principali da mostrare nei box
                    prezzo_corrente = df['Close'].iloc[-1]
                    prezzo_precedente = df['Close'].iloc[-2]
                    variazione_percentuale = ((prezzo_corrente - prezzo_precedente) / prezzo_precedente) * 100
                    
                    # Mostra i box con i dati (KPI)
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Prezzo Attuale", f"${prezzo_corrente:.2f}", f"{variazione_percentuale:.2f}%")
                    col2.metric("Massimo nel Periodo", f"${df['High'].max():.2f}")
                    col3.metric("Minimo nel Periodo", f"${df['Low'].min():.2f}")
                    
                    # Creazione del grafico interattivo a candele (Candlestick) con Plotly
                    grafico = go.Figure(data=[go.Candlestick(
                        x=df.index, open=df['Open'], high=df['High'],
                        low=df['Low'], close=df['Close'], name=ticker
                    )])
                    grafico.update_layout(
                        title=f"Andamento Storico delle Quotazioni per {ticker}",
                        xaxis_rangeslider_visible=False,
                        template="plotly_dark",
                        height=500
                    )
                    st.plotly_chart(grafico, use_container_width=True)
                else:
                    st.error("⚠️ Nessun dato trovato. Verifica che il Ticker sia corretto (es. AAPL, TSLA, BTC-USD).")
            except Exception as e:
                st.error("Si è verificato un errore durante il recupero dei dati del titolo.")

# ====================================================
# PAGINA 2: NOTIZIE E AGGIORNAMENTI
# ====================================================
elif sezione == "2. Notizie di Mercato":
    st.title("📰 Notizie e Aggiornamenti Real-Time")
    st.write("Rimani aggiornato sulle ultime novità macroeconomiche e finanziarie globali.")
    
    import urllib.request
    import xml.etree.ElementTree as ET
    
    with st.spinner("Scaricamento ultime notizie finanziarie..."):
        try:
            # Feed RSS ufficiale di Google News per la sezione Economia/Finanza in Italia
            url_feed = "https://google.com"
            
            # Mascheriamo la richiesta simulando un browser desktop standard
            req = urllib.request.Request(
                url_feed, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                
            # Parsing dell'XML ricevuto dal feed
            root = ET.fromstring(xml_data)
            articoli = root.findall('.//item')
            
            if articoli:
                st.subheader("🔥 Ultime notizie dal mondo economico e mercati")
                # Mostriamo i primi 6 articoli freschi di giornata
                for item in articoli[:6]:
                    titolo = item.find('title').text
                    link = item.find('link').text
                    data_pubb = item.find('pubDate').text if item.find('pubDate') is not None else "Ora recente"
                    fonte = item.find('source').text if item.find('source') is not None else "Google News"
                    
                    with st.expander(titolo):
                        st.write(f"**Fonte:** {fonte} | **Pubblicato il:** {data_pubb}")
                        st.write(f"[Leggi l'articolo completo direttamente alla fonte]({link})")
            else:
                st.info("Nessun aggiornamento disponibile al momento. Riprova tra pochi minuti.")
                
        except Exception as e:
            # Se il cloud fa ostruzione totale, mostriamo un aggregatore statico elegante
            st.info("📌 **Canali di Aggiornamento Consigliati:**")
            st.write("Per visualizzare i dettagli in tempo reale senza restrizioni di rete del server cloud, puoi consultare direttamente i canali istituzionali:")
            st.markdown("- [Il Sole 24 Ore - Finanza ed Economia](https://ilsole24ore.com)")
            st.markdown("- [Yahoo Finance Italia](https://yahoo.com)")
            st.markdown("- [Milano Finanza](https://milanofinanza.it)")

# ====================================================
# PAGINA 3: VALUTAZIONE INVESTIMENTO (FATTIBILITÀ)
# ====================================================
elif sezione == "3. Simulatore Investimenti":
    st.title("💰 Valutazione e Fattibilità dell'Investimento")
    st.write("Calcola l'impatto e il valore creato nel tempo grazie alla forza dell'interesse composto.")
    
    # Input dei dati da parte dell'utente organizzati su due colonne
    c_input1, c_input2 = st.columns(2)
    with c_input1:
        capitale_iniziale = st.number_input("Capitale Iniziale da investire (€):", min_value=0.0, value=5000.0, step=500.0)
        deposito_mensile = st.number_input("Piano di Accumulo / Versamento Mensile (€):", min_value=0.0, value=200.0, step=50.0)
    with c_input2:
        rendimento_annuo = st.slider("Rendimento Annuo Stimato del Portafoglio (%):", min_value=0.0, max_value=25.0, value=8.0, step=0.5)
        anni = st.slider("Orizzonte Temporale dell'Investimento (Anni):", min_value=1, max_value=40, value=10)
    
    # Logica di calcolo matematico (Mese per mese)
    mesi_totali = anni * 12
    tasso_mensile = (1 + rendimento_annuo / 100) ** (1 / 12) - 1
    
    storico_valore = [capitale_iniziale]
    storico_versamenti = [capitale_iniziale]
    
    for mese in range(1, mesi_totali + 1):
        # Formula interesse composto mensile + nuovo versamento
        nuovo_valore = storico_valore[-1] * (1 + tasso_mensile) + deposito_mensile
        storico_valore.append(nuovo_valore)
        storico_versamenti.append(storico_versamenti[-1] + deposito_mensile)
    
    valore_finale = storico_valore[-1]
    totale_versato = storico_versamenti[-1]
    interessi_guadagnati = valore_finale - totale_versato
    
    # Mostra i risultati finali della simulazione
    st.markdown("### 📈 Risultati della Proiezione di Crescita")
    res1, res2, res3 = st.columns(3)
    res1.metric("Capitale Finale Stimato", f"€{valore_finale:,.2f}")
    res2.metric("Capitale Totale Versato", f"€{totale_versato:,.2f}")
    res3.metric("Valore Creato (Interessi Maturati)", f"€{interessi_guadagnati:,.2f}", 
                delta=f"+{((interessi_guadagnati / totale_versato) * 100):.1f}% rispetto ai versamenti")
    
    # Grafico Lineare di Proiezione della crescita
    df_simulazione = pd.DataFrame({
        "Anni": np.array(range(mesi_totali + 1)) / 12,
        "Valore Portafoglio": storico_valore,
        "Capitale Versato": storico_versamenti
    })
    
    fig_crescita = go.Figure()
    fig_crescita.add_trace(go.Scatter(x=df_simulazione["Anni"], y=df_simulazione["Valore Portafoglio"], name="Valore di Mercato (Capitale + Interessi)", line=dict(color='#00FFCC', width=3)))
    fig_crescita.add_trace(go.Scatter(x=df_simulazione["Anni"], y=df_simulazione["Capitale Versato"], name="Capitale Effettivamente Versato", line=dict(color='#FF5733', dash='dash')))
    
    fig_crescita.update_layout(
        title="Proiezione della crescita del Capitale nel tempo",
        xaxis_title="Anni di Investimento",
        yaxis_title="Valore Totale (€)",
        template="plotly_dark",
        height=450
    )
    st.plotly_chart(fig_crescita, use_container_width=True)
