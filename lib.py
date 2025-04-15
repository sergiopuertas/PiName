import streamlit as st
import requests

def togglebutton():
    """
    Crea un botón de alternancia (toggle button) en Streamlit.
    """
    st.session_state.is_searching = not st.session_state.is_searching


def format_num(num):
    """
    Formatea un número entero a una cadena con separadores de miles.
    """
    return f"{int(num):,}".replace(",", ".")

def texto_a_numeros(texto: str, alg :str) -> str:
    """
    Convierte un texto a una cadena numérica donde cada letra se reemplaza
    por su posición en la clasificación de letras del alfabeto español por frecuencia de aparición.
    Luego, se convierten a número en base 27.
    Se ignoran caracteres no alfabéticos.
    """
    if alg == "Compleja":
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
    else:
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
def buscar_en_pi(pattern,_status, url="https://stuff.mit.edu/afs/sipb/contrib/pi/pi-billion.txt"):

    buffer_size = 1024 * 1024  # 1MB chunks
    position = 0
    remainder = ""

    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=buffer_size):

            text = remainder + chunk.decode('utf-8', errors='ignore')
            idx = text.replace(".","").find(pattern)
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


"""
Reference:
https://www.angio.net/pi/whynotpi.html
"""
def estimar_probabilidad(longitud: int) -> float:
    if longitud <= 6:
        return 1.0
    elif longitud == 7:
        return 0.9999995
    elif longitud == 8:
        return 0.9995
    elif longitud == 9:
        return 0.63
    elif longitud == 10:
        return 0.095
    elif longitud == 11:
        return 0.01
    else:
        return 0.001  # menor al 0.1% para 12 o más

