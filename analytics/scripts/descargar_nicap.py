import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time


def descargar_nicap_12_mes_disponibles(max_busqueda_meses=24):
    """
    Descarga los últimos 12 PDFs disponibles (no necesariamente los últimos 12 meses calendario),
    buscando hacia atrás hasta 'max_busqueda_meses' (por defecto 36).
    """
    # Obtén la carpeta donde se encuentra ESTE script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Carpeta donde se guardarán los PDFs
    base_folder = os.path.join(script_dir, "pdfs")

    # URL base de los PDFs en FINE
    base_url = "https://www.fine.com.mx/icap"

    # Diccionario (mes -> (subcarpeta, prefijo archivo))
    month_map = {
        1: ("ene", "ENE"),
        2: ("feb", "FEB"),
        3: ("mar", "MAR"),
        4: ("abr", "ABR"),
        5: ("may", "MAY"),
        6: ("jun", "JUN"),
        7: ("jul", "JUL"),
        # Para agosto, subcarpeta 'ago', pero archivo "AGOS {year}.pdf"
        8: ("ago", "AGOS"),
        9: ("sep", "SEP"),
        10: ("oct", "OCT"),
        11: ("nov", "NOV"),
        12: ("dic", "DIC"),
    }

    # Crear la carpeta si no existe
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    now = datetime.now()
    pdfs_descargados = 0
    meses_busqueda = 0

    while pdfs_descargados < 12 and meses_busqueda < max_busqueda_meses:
        date_ = now - relativedelta(months=meses_busqueda)
        year_ = date_.year
        month_num = date_.month

        # Mapeamos
        if month_num in month_map:
            folder_str, file_prefix = month_map[month_num]
        else:
            # Si no lo tenemos mapeado, pasamos al siguiente mes
            meses_busqueda += 1
            continue

        # Construimos el nombre final del PDF, por ejemplo "AGOS 2024.pdf"
        pdf_name = f"{file_prefix} {year_}.pdf"
        # Y la URL: "https://www.fine.com.mx/icap/2024/ago/AGOS 2024.pdf"
        pdf_url = f"{base_url}/{year_}/{folder_str}/{pdf_name}"

        try:
            response = requests.get(pdf_url)
            if response.status_code == 200:
                pdf_path = os.path.join(base_folder, pdf_name)
                if not os.path.exists(pdf_path):
                    with open(pdf_path, "wb") as f:
                        f.write(response.content)
                    print(f"Descargado: {pdf_name}")
                else:
                    print(f"Ya existía, se omite descarga: {pdf_name}")

                pdfs_descargados += 1
            else:
                print(f"No disponible ({response.status_code}): {pdf_name}")

        except Exception as e:
            print(f"Ocurrió un error al descargar {pdf_name}: {e}")

        meses_busqueda += 1

    print(f"Proceso terminado. PDFs descargados: {pdfs_descargados}")


def limpiar_archivos_antiguos(directorio, dias=30):
    # Tiempo actual en segundos
    ahora = time.time()

    # Iterar sobre los archivos en el directorio
    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        # Verifica si es un archivo
        if os.path.isfile(ruta_archivo):
            # Obtener el tiempo de modificación del archivo
            tiempo_modificacion = os.path.getmtime(ruta_archivo)
            # Eliminar si el archivo es más antiguo que el número de días especificado
            if ahora - tiempo_modificacion > dias * 86400:  # 86400 segundos en un día
                os.remove(ruta_archivo)
                print(f"Archivo eliminado: {ruta_archivo}")


if __name__ == "__main__":
    descargar_nicap_12_mes_disponibles()
    pdfs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
    limpiar_archivos_antiguos(pdfs_folder, dias=30)
