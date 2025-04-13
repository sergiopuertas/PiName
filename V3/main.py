import streamlit as st
from lib import buscar_en_pi, texto_a_numeros, format_num

# Inject custom CSS to include a custom font and style the page
st.markdown(
    """
    <style>
    /* Importing a custom font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Applying the custom font across the app */
    body, .main-container {
        font-family: 'Roboto', sans-serif;
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
    h1, h2, h3 {
        text-align: center;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("PiName")
st.header("Encuentra tu nombre entre los dígitos de Pi")

# Text input for the name
name = st.text_input("Ingresa tu nombre", key="pi_name",
                     help="Escribe tu nombre aquí y descubre su ubicación en los dígitos de Pi")

num = texto_a_numeros(name)
if num:
    st.write(f"Representación numérica del nombre: {format_num(num)}")
    result = buscar_en_pi(num)

    st.header("Resultado")
    if result == -1:
        st.write("No se encontró tu nombre en los primeros 1 billón de dígitos de Pi. ¡Un nombre muy peculiar!")
    else:

        result_formatted = format_num(result)
        st.write(f"Tu nombre fue encontrado en la posición: **{result_formatted}**")

st.markdown("</div>", unsafe_allow_html=True)
