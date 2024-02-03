# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/Conecta2.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

# git remote set-url origin https://github.com/nicoig/Conecta2.git
# git remote -v
# git push -u origin main


################################################
##


import streamlit as st
from dotenv import load_dotenv
import openai
import os

# Cargar las variables de entorno para las claves API
load_dotenv()

# Inicializar API de OpenAI con la clave API desde las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    st.error("No se encontró la clave API de OpenAI. Por favor, asegúrate de que está configurada correctamente.")
else:
    openai.api_key = OPENAI_API_KEY

# Configura el título y subtítulo de la aplicación en Streamlit
st.title("Conecta2: Descubre y Profundiza")
st.markdown("""
    <style>
    .small-font {
        font-size:18px !important;
    }
    </style>
    <p class="small-font">Descubre Conecta2, donde cada pregunta es una puerta a la conexión profunda. Ideal para parejas, amigos o nuevos encuentros, este juego utiliza inteligencia artificial para adaptar preguntas a tu relación específica, promoviendo descubrimientos y fortaleciendo lazos. Configura el contexto y sumérgete en un viaje de autodescubrimiento y conexión genuina.</p>
    """, unsafe_allow_html=True)

# Selecciones del usuario
estado_relacion = st.selectbox("Tu estado de relación:", ["Amigos", "Pareja recién conociéndose", "Pareja a largo plazo", "Colegas", "Familia"])
categoria_pregunta = st.selectbox("Categoría de pregunta:", ["Conociéndonos", "Aventuras Compartidas", "Valores y Sueños", "Risas y Curiosidades", "Desafíos y Opiniones"])
nivel_profundidad = st.slider("Selecciona el nivel de profundidad de las preguntas:", 1, 10, 5)

# Generar pregunta basada en selecciones
if st.button("Generar Pregunta"):
    with st.spinner('Generando tu pregunta...'):
        prompt_text = f"""
        Eres un asistente inteligente que ayuda a las personas a profundizar en sus relaciones a través de preguntas significativas.
        Debes responder sólo con la pregunta según corresponda y nada más.
        Aquí hay una guía sobre cómo cada tipo de relación y categoría debe influir en las preguntas:

        - "Amigos": Preguntas que pueden explorar experiencias compartidas, intereses comunes, o cómo se conocieron. Ejemplo: "¿Cuál es un recuerdo feliz que compartimos que aún te hace sonreír?"
        - "Pareja recién conociéndose": Preguntas para ayudar a descubrir nuevas facetas el uno del otro. Ejemplo: "¿Cuál es una pasión tuya que aún no he descubierto?"
        - "Pareja a largo plazo": Enfócate en preguntas que reaviven la chispa o profundicen en aspectos no explorados de su relación. Ejemplo: "¿Qué aventura aún no hemos vivido juntos que te gustaría experimentar?"
        - "Colegas": Preguntas que fomenten la construcción de un equipo sólido y la comprensión mutua. Ejemplo: "¿Cuál crees que es nuestra mayor fortaleza como equipo y cómo podemos aprovecharla aún más?"
        - "Familia": Preguntas para fortalecer los lazos y comprender mejor las dinámicas familiares. Ejemplo: "¿Cuál es un valor familiar que crees que todos compartimos y cómo lo demostramos?"

        Considerando que el nivel de profundidad deseado es {nivel_profundidad}, donde 1 es superficial y 10 muy íntimo o profundo, por favor, genera una pregunta adecuada para "{estado_relacion}" dentro de la categoría "{categoria_pregunta}" sin mencionar el nivel de profundidad en la respuesta.
        """

        try:
            # Realizar la llamada a la API de OpenAI para generar la pregunta utilizando el modelo gpt-3.5-turbo
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "system", "content": prompt_text},
                  {"role": "user", "content": "Por favor, genera una pregunta para la situación descrita."},
              ]
            )
            
            # Extraer la pregunta generada
            pregunta_generada = response.choices[0].message['content']
            
            # Mostrar la pregunta generada sin incluir el nivel de profundidad explicitamente
            st.markdown("**Pregunta generada:**")
            st.write(pregunta_generada)
        except Exception as e:
            st.error(f"Se produjo un error al generar la pregunta: {e}")
