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
    por su posición en la clasificación de letras del alfabeto español por frecuencia de aparición.
    Luego, se convierten a número en base 27.
    Se ignoran caracteres no alfabéticos.
    """
    alfabeto = {
        "a":1, "á":1, "e":2, "é":2, "o":3, "ó":3, "i":4, "í":4, "n":5, "l":6, "s":7, "r":8, "m":9,
        "d":10, "c":11, "u":12, "ú":12, "ü":12, "t":13, "p":14, "b":15, "g":16, "y":17, "ý":17, "j":18, "h":19, "v":20,
        "z":21, "q":22, "f":23, "ñ":24, "x":25, "k":26, "w":27
    }
    base = 27
    valor = 0
    for c in texto.lower():
        if c in alfabeto:
            valor = valor * base + alfabeto[c]
    return str(valor)

@st.cache_data(show_spinner=False, ttl=3600)
def buscar_en_pi(pattern,_status, url="https://stuff.mit.edu/afs/sipb/contrib/pi/pi-billion.txt"):

    buffer_size = 1024 * 1024  # 1MB chunks
    position = 0
    remainder = ""

    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=buffer_size):
            text = remainder + chunk.decode('utf-8', errors='ignore')
            idx = text.find(pattern)
            if idx != -1:
                start_context = max(0, idx - 5)
                end_context = idx + len(pattern) + 5
                context = text[start_context:end_context]
                return position + idx + 1, context  # 1-indexed

            remainder = text[-len(pattern):]
            position += buffer_size
            result_formatted = format_num(position)
            _status.update(label = f"🔍 Explorados hasta ahora: `{result_formatted}` dígitos...")
    return -1 , None  # no encontrado
