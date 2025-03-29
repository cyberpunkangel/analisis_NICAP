import os
import pdfplumber
import pandas as pd


def parse_pdf_nicap(pdf_path):
    """
    Extrae la tabla NICAP de un PDF y regresa una lista de diccionarios con la información.
    Asume que la tabla está en la página 0 y que la estructura es consistente (2 filas de encabezado).
    """
    rows_data = []  # aquí guardaremos dicts con los campos de cada fila

    with pdfplumber.open(pdf_path) as pdf:
        # normalmente es una sola página
        page = pdf.pages[0]
        tables = page.extract_tables()

        # Suponiendo que solo hay 1 tabla principal
        if not tables:
            return rows_data  # lista vacía

        table = tables[0]
        # 'table' es una lista de listas.
        # Ej: table[0] = ['ENTIDADES', None, 'NICAP 1∕', None, 'Variación Mensual\npp 2∕', 'Categoria...']

        # En tu ejemplo, las dos primeras filas son encabezados/column headers:
        # table[0] = ...
        # table[1] = ...
        # A partir de table[2] están los datos "reales".
        data_rows = table[2:]

        # Recorremos cada fila de datos
        for row in data_rows:
            # row debería tener 6 columnas en tu ejemplo:
            #  0 -> No. (1,2,3,...)
            #  1 -> ENTIDAD
            #  2 -> NICAP mes anterior
            #  3 -> NICAP mes actual
            #  4 -> Variación
            #  5 -> Categoría
            #
            # Dependiendo de la consistencia de tus PDFs, puede variar.
            if len(row) < 6:
                continue  # si por algún motivo hay filas incompletas

            # Creamos un diccionario con los campos
            row_dict = {
                "No": row[0],
                "Entidad": row[1],
                "NICAP_Anterior": row[2],
                "NICAP_Actual": row[3],
                "Variacion": row[4],
                "Categoria": row[5],
                # Opcionalmente, registramos el nombre del PDF de origen
                "Fuente_PDF": os.path.basename(pdf_path),
            }
            rows_data.append(row_dict)

    return rows_data


def parsear_todos_los_pdfs():
    """
    Recorre la carpeta 'pdfs', busca archivos .pdf,
    los parsea con parse_pdf_nicap y luego guarda todo en un CSV (pandas).
    """
    # Carpeta donde están los PDFs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdfs_folder = os.path.join(script_dir, "pdfs")

    # Lista para acumular los resultados de TODOS los PDFs
    all_data = []

    # Recorremos todos los archivos .pdf
    for file_name in os.listdir(pdfs_folder):
        if file_name.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdfs_folder, file_name)
            # Parseamos cada PDF
            data_rows = parse_pdf_nicap(pdf_path)
            # Agregamos a la lista general
            all_data.extend(data_rows)

    # Convertimos la lista de diccionarios a un DataFrame pandas
    df = pd.DataFrame(all_data)

    # Guardamos en CSV
    csv_path = os.path.join(script_dir, "NICAP_data.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"Se procesaron {len(all_data)} filas en total.")
    print(f"CSV generado en: {csv_path}")


if __name__ == "__main__":
    # Ejecutar el parseo de todos los PDFs
    parsear_todos_los_pdfs()
