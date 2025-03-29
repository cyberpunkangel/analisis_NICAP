import pandas as pd

# Diccionario para mapear el prefijo textual al número de mes
mes_map = {
    "ENE": 1,
    "FEB": 2,
    "MAR": 3,
    "ABR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AGOS": 8,
    "AGO": 8,  # FINE a veces usa "AGOS", a veces "AGO"
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DIC": 12,
}

df = pd.read_csv("NICAP_data.csv", encoding="utf-8-sig")


def extraer_fecha_de_pdf(pdf_name):
    """
    pdf_name = "ABR 2024.pdf" o "AGOS 2024.pdf"
    1) Quitamos la extensión (.pdf)
    2) Dividimos por espacio para separar "ABR" y "2024".
    3) Convertimos a un formato "YYYY-MM" (string).
    """
    base = pdf_name.replace(".pdf", "")
    parts = base.split()
    if len(parts) < 2:
        return None

    mes_str, anio_str = parts[0].upper(), parts[1]
    if mes_str not in mes_map:
        return None

    mes_num = mes_map[mes_str]
    anio_num = int(anio_str)
    # Retornamos la cadena "YYYY-MM"
    return f"{anio_num:04d}-{mes_num:02d}"


# Asignamos la nueva columna 'Fecha' parseando el nombre del PDF
df["Fecha"] = df["Fuente_PDF"].apply(extraer_fecha_de_pdf)

# (Opcional) Creamos también una columna datetime de primer día del mes,
# para gráficas cronológicas:
df["Fecha_dt"] = pd.to_datetime(df["Fecha"] + "-01", errors="coerce")

# ---- 2. Convertir NICAP/Variacion a float ----


def convertir_a_float(val):
    """
    - Si encuentra % lo quita y convierte a float.
    - Maneja "NO SE PUEDE CALCULAR", "N/A", etc. devolviendo None.
    """
    if not isinstance(val, str):
        # Por si val ya es numérico o None
        return val

    val = val.strip().upper()
    if ("NO SE PUEDE" in val) or ("N/A" in val) or ("INFORMACIÓN" in val):
        return None

    # Quitar '%'
    val = val.replace("%", "")
    # Intentar convertir
    try:
        return float(val)
    except:
        return None


# Aplicamos la función a cada columna:
df["NICAP_Anterior"] = df["NICAP_Anterior"].apply(convertir_a_float)
df["NICAP_Actual"] = df["NICAP_Actual"].apply(convertir_a_float)
df["Variacion"] = df["Variacion"].apply(convertir_a_float)

# Modificar la columna "Categoría"
df["Categoria"] = df["Categoria"].str.extract("(\d+)")
df["Categoria"] = df["Categoria"].fillna(0).astype(int)

# Excluir columnas
df = df.drop(columns=["Fuente_PDF", "Fecha_dt"])

# ---- 3. Guardar CSV limpio ----
df.to_csv("NICAP_data_limpio.csv", index=False, encoding="utf-8-sig")
