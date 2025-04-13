import streamlit as st
import requests

def format_num(num):
    """
    Formatea un número entero a una cadena con separadores de miles.
    """
    return f"{int(num):,}".replace(",", ".")

def texto_a_numeros(texto: str) -> str:
    """
    Convierte un texto a una cadena numérica donde cada letra se reemplaza
    por su posición en el alfabeto español (a=1, b=2, …, n=14, ñ=15, o=16, ... z=27).
    Se ignoran caracteres no alfabéticos.
    """
    alfabeto = {
    "a": "1", "á": "1", "b": "2", "c": "3", "d": "4", "e": "5", "é": "5", "f": "6", "g": "7",
    "h": "8", "i": "9", "í": "9", "j": "10", "k": "11", "l": "12", "m": "13",
    "n": "14", "ñ": "15", "o": "16", "ó": "16", "p": "17", "q": "18", "r": "19",
    "s": "20", "t": "21", "u": "22", "ú": "22", "ü": "22", "v": "23", "w": "24",
        "x": "25", "y": "26", "ý": "26", "z": "27"
}
    resultado = ""
    for caracter in texto.lower():
        if caracter in alfabeto:
            resultado += alfabeto[caracter]
    return resultado

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
            result_formatted = format_num(position)
            status.update(label = f"🔍 Explorados hasta ahora: `{result_formatted}` dígitos...")

    status.update(label="🚫 Coincidencia no encontrada", state="error")
    return -1  # no encontrado
