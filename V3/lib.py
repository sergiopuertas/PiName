import streamlit as st
import requests

def texto_a_numeros(texto):
    abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    texto = texto.upper()
    return ''.join(str(abecedario.index(c) + 1).zfill(2) for c in texto if c in abecedario)

@st.cache_data(show_spinner=False, ttl=3600)
def buscar_en_pi(pattern, url="https://stuff.mit.edu/afs/sipb/contrib/pi/pi-billion.txt"):

    buffer_size = 1024 * 1024  # 1MB chunks
    position = 0
    remainder = ""

    status = st.status("Buscando coincidencia en los dígitos de π...", expanded=True)

    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=buffer_size):
            text = remainder + chunk.decode('utf-8', errors='ignore')
            idx = text.find(pattern)
            if idx != -1:
                status.update(label="✅ Coincidencia encontrada", state="complete")
                return position + idx + 1  # 1-indexed

            remainder = text[-len(pattern):]
            position += buffer_size
            result_formatted = f"{int(position):,}".replace(",", ".")
            status.update(label = f"🔍 Explorados hasta ahora: `{result_formatted}` dígitos...")

    status.update(label="🚫 Coincidencia no encontrada", state="error")
    return -1  # no encontrado
