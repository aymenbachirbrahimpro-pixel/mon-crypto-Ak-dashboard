import streamlit as st
import ccxt
import pandas as pd
import ta
import time

# Configuration de la page
st.set_page_config(page_title="Dashboard RSI Ultime - Halal Crypto", layout="wide")
st.title("🎯 Dashboard RSI Ultime - Flux Binance Spot en Temps Réel")
st.write("Calcul automatique du RSI (14) sur les 23 cryptos sélectionnées (Halal + Hyperliquid + Binance)")

# Liste exacte des 23 cryptos Halal
symbols = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT',
    'DOT/USDT', 'NEAR/USDT', 'SUI/USDT', 'APT/USDT', 'LTC/USDT', 'ICP/USDT',
    'XLM/USDT', 'HBAR/USDT', 'ATOM/USDT', 'TAO/USDT', 'WLD/USDT', 'FET/USDT',
    'ARB/USDT', 'OP/USDT', 'TIA/USDT', 'SEI/USDT', 'STX/USDT'
]

timeframes = ['5m', '15m', '1h', '4h', '1d']
exchange = ccxt.binance()

def get_rsi(symbol, timeframe):
    try:
        # Récupère les 50 dernières bougies
        bars = exchange.fetch_ohlcv(symbol, timeframe, limit=50)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        rsi_series = ta.momentum.rsi(df['close'], window=14)
        return round(rsi_series.iloc[-1], 2)
    except:
        return None

# Bouton de rafraîchissement manuel
if st.button("🔄 Rafraîchir les données"):
    st.rerun()

# Création du tableau de bord
data = []
progress_bar = st.progress(0)

for idx, symbol in enumerate(symbols):
    row = {'Crypto': symbol.split('/')[0]}
    for tf in timeframes:
        row[tf] = get_rsi(symbol, tf)
    data.append(row)
    progress_bar.progress((idx + 1) / len(symbols))

df_rsi = pd.DataFrame(data)

# Fonction pour colorer le tableau (Heatmap)
def color_rsi(val):
    if pd.isna(val):
        return ''
    elif val >= 70:
        return 'background-color: #ff4d4d; color: white; font-weight: bold;' # Rouge Surachat
    elif val <= 30:
        return 'background-color: #2ecc71; color: white; font-weight: bold;' # Vert Survente
    elif val >= 65:
        return 'background-color: #ff9999; color: black;' # Proche surachat
    elif val <= 35:
        return 'background-color: #a3e4d7; color: black;' # Proche survente
    return ''

# Affichage stylisé
styled_df = df_rsi.style.applymap(color_rsi, subset=timeframes)
st.dataframe(styled_df, height=850, use_container_width=True)

st.caption("Légende : 🔴 Rouge = Surachat (RSI ≥ 70) | 🟢 Vert = Survente (RSI ≤ 30) | Données en direct de l'API Binance Spot.")

# Lancement de l'application locale (Utile pour Google Colab)
import os
if _name_ == '_main_':
    with open("app.py", "w") as f:
        f.write(open(_file_).read())
    os.system("npx localtunnel --port 8501 & streamlit run app.py --server.port 8501")
