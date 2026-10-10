import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. Configurazione della pagina (Titolo della scheda del browser)
st.set_page_config(page_title="Il mio Portafoglio Finanziario", layout="wide")

# 2. Creazione del Menu Laterale di navigazione
st.sidebar.title("Navigazione Portafoglio")
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
    st.write("Rimani aggiornato sulle ultime novità societarie e macroeconomiche.")
    
    ticker_news = st.text_input("Filtra le notizie per Ticker aziendale:", "AAPL").upper()
    
    if ticker_news:
        with st.spinner("Ricerca notizie..."):
            try:
                dati_titolo = yf.Ticker(ticker_news)
                lista_notizie = dati_titolo.news
                
                # Se yfinance restituisce notizie valide, mostriamo quelle del ticker
                if lista_notizie and len(lista_notizie) > 0:
                    st.subheader(f"Ultime notizie rilevanti per {ticker_news}")
                    for news in lista_notizie[:5]:
                        with st.expander(news['title']):
                            st.write(f"**Fonte:** {news.get('publisher', 'N/D')}")
                            data_pubb = pd.to_datetime(news.get('providerPublishTime', 0), unit='s')
                            st.write(f"**Data di pubblicazione:** {data_pubb.strftime('%d/%m/%Y %H:%M')}")
                            st.write(f"[Clicca qui per leggere l'articolo completo]({news['link']})")
                
                # FALLBACK: Se yfinance fallisce o è bloccato sul cloud, carichiamo le notizie generali di mercato
                else:
                    st.warning(f"⚠️ Limitazione temporanea sui server per il ticker {ticker_news}. Mostro le ultime notizie Generali di Mercato:")
                    dati_generali = yf.Ticker("SPY") # Usiamo l'indice S&P 500 come paracadute generale
                    news_generali = dati_generali.news
                    
                    if news_generali:
                        for news in news_generali[:5]:
                            with st.expander(news['title']):
                                st.write(f"**Fonte:** {news.get('publisher', 'N/D')}")
                                data_pubb = pd.to_datetime(news.get('providerPublishTime', 0), unit='s')
                                st.write(f"**Data di pubblicazione:** {data_pubb.strftime('%d/%m/%Y %H:%M')}")
                                st.write(f"[Clicca qui per leggere l'articolo completo]({news['link']})")
                    else:
                        st.info("Nessuna notizia disponibile al momento. Riprova tra pochi minuti.")
            except Exception as e:
                st.error("Impossibile recuperare le notizie al momento a causa di restrizioni del server.")

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
