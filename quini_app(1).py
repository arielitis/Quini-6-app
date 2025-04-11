
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Análisis de Resultados del Quini 6")

@st.cache_data
def cargar_datos():
    url = "https://www.loteriadesantafe.gov.ar/api/api_get_sorteos.php?juego=QUINI6"
    return pd.read_json(url)

df = cargar_datos()

# Filtrar solo columnas relevantes y convertir los resultados en listas de números
df['numeros'] = df['resultados'].apply(lambda x: list(map(int, x.split(','))))
todos_los_numeros = [num for sublist in df['numeros'] for num in sublist]

# Conteo de frecuencias
frecuencia = pd.Series(todos_los_numeros).value_counts().sort_index()

st.subheader("Frecuencia de aparición de cada número")
st.bar_chart(frecuencia)

# Heatmap por decena y unidad
df_heat = pd.DataFrame(columns=range(0,10), index=["0-9", "10-19", "20-29", "30-39", "40-45"])
df_heat = df_heat.fillna(0)

for n in frecuencia.index:
    freq = frecuencia[n]
    decena = f"{(n//10)*10}-{(n//10)*10 + 9}" if n < 40 else "40-45"
    col = n % 10
    df_heat.loc[decena, col] = freq

st.subheader("Heatmap de frecuencia por decenas y unidades")
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(df_heat, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# Proporción pares e impares
pares = [n for n in todos_los_numeros if n % 2 == 0]
impares = [n for n in todos_los_numeros if n % 2 != 0]

st.subheader("Proporción total de pares e impares")
st.write(f"Pares: {len(pares)} ({len(pares) / len(todos_los_numeros) * 100:.2f}%)")
st.write(f"Impares: {len(impares)} ({len(impares) / len(todos_los_numeros) * 100:.2f}%)")
