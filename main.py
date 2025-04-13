import streamlit as st
from lib import buscar_en_pi, texto_a_numeros, format_num

# Set the page configuration
st.set_page_config(
    page_title="PiName",
    page_icon=":pie:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS to include a custom font and style the page
st.markdown(
    """
    <style>
    /* Importing a custom font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Applying the custom font across the app */
    body, .main-container {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
    }

    /* Optional: Additional styling */
    .main-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem auto;
        width: 80%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3, h4, h5 {
        text-align: center;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(f"<h1 style='text-align: center; font-size: 5rem;'>PiName</h1>",
            unsafe_allow_html=True)

st.header("Encuentra tu nombre entre los dígitos de Pi")

# Text input for the name
name = st.text_input("Ingresa tu nombre", key="pi_name",
                     help="Tu nombre se convierte una cadena numérica donde cada letra se reemplaza"
    " por su posición en la clasificación de letras del alfabeto español por frecuencia de aparición: a, e, o, i, n, l,"
    " s, r, m, d, c, u, t, p, b, g, y, j, h, v, z, q, f, ñ, x, k, w. "
    "Luego, se convierten a número en base 27 para compactarlo lo máximo posible.",placeholder=None)
num = texto_a_numeros(name)

if name != "":
    st.write(f"Representación numérica del nombre: {format_num(num)}")
    status = st.status("Buscando coincidencia en los dígitos de π...", expanded=True)
    result, text = buscar_en_pi(num,status)
    status.update(label="✅ Coincidencia encontrada", state="complete")
    if result == -1:
        status.update(label="🚫 Coincidencia no encontrada", state="error")
        st.write("No se encontró tu nombre en los primeros mil millones de dígitos de Pi. ¡Un nombre muy peculiar!")
    elif text is not None and num is not None:
       result_formatted = format_num(result)
       st.container(height=30,border=False)
       st.markdown(f"<h2 style='text-align: center; font-size: 2rem;'>Tu nombre fue encontrado en la posición:</h2>", unsafe_allow_html=True)
       st.markdown(f"<h2 style='text-align: center; font-size: 3rem;'><strong>{result_formatted}</strong></h2>", unsafe_allow_html=True)
       st.container(height=10,border=False)
       st.markdown(f"<p style='text-align: center; font-size: 2rem;'>3.141592...{str(text).replace(num, f'<strong>{num}</strong>')}...</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

