import streamlit as st
import pandas as pd
import requests
import json
import random
from collections import Counter

st.set_page_config(page_title="Quini 6 App", layout="centered")

@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/arielitis/quini6-app/main/datos.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica que la respuesta sea 200
        data = json.loads(response.text)
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos del archivo JSON: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        st.error(f"Error al interpretar el archivo JSON: {e}")
        return pd.DataFrame()

def generar_jugada_probable(df, tipo_sorteo, cantidad_jugadas=1):
    df_filtrado = df[df["tipo_sorteo"] == tipo_sorteo]

    numeros = []
    for i in range(1, 7):
        numeros += df_filtrado[f"numero_{i}"].tolist()

    conteo = Counter(numeros)
    numeros_ordenados = [num for num, _ in conteo.most_common()]
    jugadas = []

    for _ in range(cantidad_jugadas):
        jugada = sorted(random.sample(numeros_ordenados[:30], 6))
        jugadas.append(jugada)

    return jugadas

# --- Interfaz ---
st.title("Generador de Jugadas Probables - Quini 6")

df = cargar_datos()
tipos_sorteo = df["tipo_sorteo"].unique().tolist()

tipo_sorteo_seleccionado = st.selectbox("Seleccioná el tipo de sorteo", tipos_sorteo)
cantidad_jugadas = st.slider("Cantidad de jugadas a generar", 1, 10, 3)

if st.button("Generar jugadas"):
    jugadas = generar_jugada_probable(df, tipo_sorteo_seleccionado, cantidad_jugadas)
    for i, jugada in enumerate(jugadas, start=1):
        st.success(f"Jugada #{i}: {', '.join(map(str, jugada))}")
