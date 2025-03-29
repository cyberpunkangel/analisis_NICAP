import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .scripts.analisis_nicap import obtener_datos_y_graficos

def analisis_nicap(request):
    tabla_html, grafico_uri, grafico_pie_uri = obtener_datos_y_graficos()
    contexto = {
        "tabla": tabla_html,
        "grafico": grafico_uri,
        "grafico_pie": grafico_pie_uri,
    }
    return render(request, "nicap.html", contexto)


def descargar_csv(request):
    # Construye la ruta al archivo de forma dinámica
    csv_path = os.path.join(settings.BASE_DIR, 'analytics', 'scripts', 'NICAP_data_limpio.csv')

    # Lee el archivo CSV
    df = pd.read_csv(csv_path)
    
    # Prepara la respuesta HTTP
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="NICAP_data.csv"'
    # Escribe el DataFrame en la respuesta                                      
    df.to_csv(path_or_buf=response, index=False)
    return response
