import pandas as pd
import plotly.express as px
import os
import re


def obtener_datos_y_graficos():
    # Obtén la carpeta donde se encuentra ESTE script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "NICAP_data_limpio.csv")

    # Cargar el CSV
    df = pd.read_csv(csv_path)
    # Crear una copia para el gráfico
    df_grafico = df.copy()

    # Crear una columna para identificar entidades similares
    df_grafico["Entidad_Key"] = (
        df_grafico["Entidad"]
        .str[:20]
        .str.replace(r"[\*\/]+", "", regex=True)
        .str.strip()
    )

    # Encontrar el nombre completo más largo para cada grupo similar
    df_grafico["Entidad_Normalizada"] = df_grafico.groupby("Entidad_Key")[
        "Entidad"
    ].transform(lambda x: x.loc[x.str.len().idxmax()])

    # Limpiar los caracteres no deseados al final de los nombres
    df_grafico["Entidad_Normalizada"] = df_grafico["Entidad_Normalizada"].apply(
        lambda x: re.sub(r"[\*\/]+$", "", x).strip()
    )

    # Agrupar por Entidad_Normalizada y calcular la media de NICAP_Actual
    df_grafico = df_grafico.groupby(["Entidad_Normalizada", "Fecha"], as_index=False)[
        "NICAP_Actual"
    ].mean()

    # Crear gráfico interactivo con Plotly
    fig = px.line(
        df_grafico,
        x="Fecha",
        y="NICAP_Actual",
        color="Entidad_Normalizada",
        markers=True,
        labels={"NICAP_Actual": "NICAP Actual"},
        hover_name="Entidad_Normalizada",
    )

    fig.update_layout(
        title="NICAP Actual por Entidad",
        xaxis_title="Periodo",
        yaxis_title="NICAP Actual",
        legend_title_text="Entidades",
        xaxis=dict(tickangle=45),
    )

    # Convertir gráfico a HTML
    grafico_html = fig.to_html(full_html=False)

    # Formatear para la tabla sin modificar
    df_tabla = df.copy()
    for col in ["NICAP_Anterior", "NICAP_Actual", "Variacion"]:
        df_tabla[col] = df_tabla[col].round(2).astype(str) + "%"

    # Ordenar para la tabla
    df_tabla = df_tabla.sort_values(by=["Fecha", "No"], ascending=[False, True])

    # Convertir DataFrame a HTML
    tabla_html = df_tabla.to_html(classes="table table-striped", index=False)

    return tabla_html, grafico_html
