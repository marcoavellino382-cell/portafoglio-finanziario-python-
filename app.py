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

# Aggiunge il logo nella sidebar permettendoti di impostare la larghezza su misura
st.sidebar.image("logo.png", width=150)

# 2. Creazione del Menu Laterale di navigazione
st.sidebar.title("Portfolio Manager")
sezione = st.sidebar.radio("Menu di Navigazione", ["Titoli e Grafici", "Notizie di Mercato", "Simulatore Investimenti", "Bilanciamento Portafoglio"])

# Elementi grafici di chiusura per la Sidebar
st.sidebar.markdown("---")
st.sidebar.caption("🤖 **Stato Sistema:** Operativo (Cloud)")
st.sidebar.caption("📦 **Versione:** v1.2.0 (Stable)")
st.sidebar.markdown("👨‍💻 **Sviluppato da:** [Marco Avellino](https://linkedin.com/in/marco-avellino-1a0918411)")

# ====================================================
# PAGINA 1: TITOLI FINANZIARI E GRAFICI
# ====================================================
if sezione == "Titoli e Grafici":
    st.title("📊 Analisi Titoli e Grafici Interattivi")
    st.write("Inserisci il codice di un titolo azionario o crypto per visualizzare i dati in tempo reale.")
    
    ticker = st.text_input("Inserisci il codice Ticker del titolo (es. AAPL, TSLA, BTC-USD):", "AAPL").upper()
    periodo = st.selectbox("Seleziona l'orizzonte temporale del grafico:", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
    
    if ticker:
        with st.spinner("Scaricamento dati in corso..."):
            try:
                dati_titolo = yf.Ticker(ticker)
                df = dati_titolo.history(period=periodo)
                
                if not df.empty and len(df) > 1:
                    prezzo_corrente = df['Close'].iloc[-1]
                    prezzo_precedente = df['Close'].iloc[-2]
                    variazione_percentuale = ((prezzo_corrente - prezzo_precedente) / prezzo_precedente) * 100
                    
                    # LOGICA VALUTA DINAMICA: controlla se il titolo è quotato in Euro o Dollari
                    try:
                        valuta_nativa = dati_titolo.info.get('currency', 'USD')
                    except:
                        valuta_nativa = 'USD'
                        
                    simbolo = "€" if valuta_nativa == "EUR" else "$" if valuta_nativa == "USD" else f"{valuta_nativa} "
                    
                    # Mostra i box con la valuta dinamica corretta
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Prezzo Attuale", f"{simbolo}{prezzo_corrente:.2f}", f"{variazione_percentuale:.2f}%")
                    col2.metric("Massimo nel Periodo", f"{simbolo}{df['High'].max():.2f}")
                    col3.metric("Minimo nel Periodo", f"{simbolo}{df['Low'].min():.2f}")
                    
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
elif sezione == "Notizie di Mercato":
    st.title("📰 Notizie e Aggiornamenti Real-Time")
    st.write("Rimani aggiornato sulle ultime novità macroeconomiche e finanziarie globali.")
    
    import urllib.request
    import xml.etree.ElementTree as ET
    
    with st.spinner("Scaricamento ultime notizie finanziarie..."):
        try:
            url_feed = "https://google.com"
            req = urllib.request.Request(
                url_feed, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            articoli = root.findall('.//item')
            
            if articoli:
                st.subheader("🔥 Ultime notizie dal mondo economico e mercati")
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
            st.info("📌 **Canali di Aggiornamento Consigliati:**")
            st.write("Per visualizzare i dettagli in tempo reale senza restrizioni di rete del server cloud, puoi consultare direttamente i canali istituzionali:")
            st.markdown("- [Il Sole 24 Ore - Finanza ed Economia](https://ilsole24ore.com)")
            st.markdown("- [Yahoo Finance Italia](https://yahoo.com)")
            st.markdown("- [Milano Finanza](https://milanofinanza.it)")

# ====================================================
# PAGINA 3: VALUTAZIONE INVESTIMENTO (FATTIBILITÀ)
# ====================================================
elif sezione == "Simulatore Investimenti":
    st.title("💰 Valutazione e Fattibilità dell'Investimento")
    st.write("Calcola l'impatto e il valore creato nel tempo grazie alla forza dell'interesse composto.")
    
    c_input1, c_input2 = st.columns(2)
    with c_input1:
        capitale_iniziale = st.number_input("Capitale Iniziale da investire (€):", min_value=0.0, value=5000.0, step=500.0)
        deposito_mensile = st.number_input("Piano di Accumulo / Versamento Mensile (€):", min_value=0.0, value=200.0, step=50.0)
    with c_input2:
        rendimento_annuo = st.slider("Rendimento Annuo Stimato del Portafoglio (%):", min_value=0.0, max_value=25.0, value=8.0, step=0.5)
        anni = st.slider("Orizzonte Temporale dell'Investimento (Anni):", min_value=1, max_value=40, value=10)
    
    mesi_totali = anni * 12
    tasso_mensile = (1 + rendimento_annuo / 100) ** (1 / 12) - 1
    
    storico_valore = [capitale_iniziale]
    storico_versamenti = [capitale_iniziale]
    
    for mese in range(1, mesi_totali + 1):
        nuovo_valore = storico_valore[-1] * (1 + tasso_mensile) + deposito_mensile
        storico_valore.append(nuovo_valore)
        storico_versamenti.append(storico_versamenti[-1] + deposito_mensile)
    
    valore_finale = storico_valore[-1]
    totale_versato = storico_versamenti[-1]
    interessi_guadagnati = valore_finale - totale_versato
    
    st.markdown("### 📈 Risultati della Proiezione di Crescita")
    res1, res2, res3 = st.columns(3)
    res1.metric("Capitale Finale Stimato", f"€{valore_finale:,.2f}")
    res2.metric("Capitale Totale Versato", f"€{totale_versato:,.2f}")
    res3.metric("Valore Creato (Interessi Maturati)", f"€{interessi_guadagnati:,.2f}", 
                delta=f"+{((interessi_guadagnati / totale_versato) * 100):.1f}% rispetto ai versamenti")
    
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
    
# ====================================================
# PAGINA 4: ASSET ALLOCATION E RIBILANCIAMENTO
# ====================================================
elif sezione == "Bilanciamento Portafoglio":
    st.title("⚖️ Asset Allocation & Ribilanciamento Strategico")
    st.write("Imposta i tuoi obiettivi di portafoglio e calcola esattamente come ribilanciare il capitale attuale.")
    
    # 1. Configurazione delle percentuali obiettivo (Target Allocation)
    st.subheader("1. Imposta la tua Asset Allocation Obiettivo (%)")
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    
    with col_t1:
        target_azioni = st.number_input("Azioni / ETF (%):", min_value=0.0, max_value=100.0, value=60.0, step=5.0)
    with col_t2:
        target_obbligazioni = st.number_input("Obbligazioni (%):", min_value=0.0, max_value=100.0, value=20.0, step=5.0)
    with col_t3:
        target_oro = st.number_input("Oro / Beni Rifugio (%):", min_value=0.0, max_value=100.0, value=10.0, step=5.0)
    with col_t4:
        target_crypto = st.number_input("Crypto / Liquidità (%):", min_value=0.0, max_value=100.0, value=10.0, step=5.0)
        
    totale_target = target_azioni + target_obbligazioni + target_oro + target_crypto
    
    # Controllo di sicurezza matematico
    if totale_target != 100.0:
        st.warning(f"⚠️ La somma delle percentuali obiettivo deve fare esattamente 100%. Attualmente è: {totale_target}%")
    else:
        st.success("✅ Asset Allocation impostata correttamente (Totale 100%).")
        
        # 2. Inserimento del valore attuale del portafoglio
        st.markdown("---")
        st.subheader("2. Inserisci il Valore Attuale del tuo Portafoglio (€)")
        
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)
        with col_v1:
            valore_azioni = st.number_input("Valore Attuale Azioni (€):", min_value=0.0, value=5500.0, step=100.0)
        with col_v2:
            valore_obbligazioni = st.number_input("Valore Attuale Obbligazioni (€):", min_value=0.0, value=2500.0, step=100.0)
        with col_v3:
            valore_oro = st.number_input("Valore Attuale Oro (€):", min_value=0.0, value=800.0, step=100.0)
        with col_v4:
            valore_crypto = st.number_input("Valore Attuale Crypto (€):", min_value=0.0, value=1200.0, step=100.0)
            
        capitale_totale = valore_azioni + valore_obbligazioni + valore_oro + valore_crypto
        st.metric("Valore Totale Portafoglio", f"€{capitale_totale:,.2f}")
        
        # 3. Logica e Calcoli di Ribilanciamento
        valori_attuali = [valore_azioni, valore_obbligazioni, valore_oro, valore_crypto]
        targets = [target_azioni, target_obbligazioni, target_oro, target_crypto]
        categorie = ["Azioni/ETF", "Obbligazioni", "Oro", "Crypto/Liquidità"]
        
        azioni_richieste = []
        
        for val_attuale, target, cat in zip(valori_attuali, targets, categorie):
            valore_teorico_obiettivo = capitale_totale * (target / 100)
            differenza = valore_teorico_obiettivo - val_attuale
            azioni_richieste.append({
                "Categoria": cat,
                "Valore Attuale": val_attuale,
                "Percentuale Attuale": (val_attuale / capitale_totale) * 100 if capitale_totale > 0 else 0,
                "Percentuale Target": target,
                "Ribilanciamento": differenza
            })
            
        df_ribilanciamento = pd.DataFrame(azioni_richieste)
        
        # 4. Visualizzazione Grafica (Confronto con Grafico a Torta / Donut Chart)
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            fig_attuale = go.Figure(data=[go.Pie(labels=df_ribilanciamento["Categoria"], values=df_ribilanciamento["Valore Attuale"], hole=.4)])
            fig_attuale.update_layout(title_text="Composizione Attuale del Portafoglio", template="plotly_dark", height=350)
            st.plotly_chart(fig_attuale, use_container_width=True)
            
        with col_g2:
            fig_target = go.Figure(data=[go.Pie(labels=df_ribilanciamento["Categoria"], values=df_ribilanciamento["Percentuale Target"], hole=.4)])
            fig_target.update_layout(title_text="Composizione Obiettivo (Target)", template="plotly_dark", height=350)
            st.plotly_chart(fig_target, use_container_width=True)
            
                # 5. Tabella dei Risultati Operativi con indicazioni Compra/Vendi
        st.subheader("📋 Azioni Correttive per il Ribilanciamento")
        st.write("Segui queste indicazioni per riallineare il tuo portafoglio agli obiettivi strategici:")
        
        for index, row in df_ribilanciamento.iterrows():
            operazione = row["Ribilanciamento"]
            if operazione > 0:
                st.info(f"➕ **{row['Categoria']}**: Devi **COMPRARE** €{operazione:,.2f} per raggiungere il target del {row['Percentuale Target']}%")
            elif operazione < 0:
                st.warning(f"➖ **{row['Categoria']}**: Devi **VENDERE** €{abs(operazione):,.2f} per scendere al target del {row['Percentuale Target']}%")
            else:
                st.success(f"🎯 **{row['Categoria']}**: Perfettamente bilanciato al {row['Percentuale Target']}%")
