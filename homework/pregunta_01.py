"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
import pandas as pd
import re

def pregunta_01():
    # Leer el archivo línea por línea
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Eliminar líneas vacías y de separación
    lines = [line.rstrip() for line in lines if line.strip() and not line.startswith('---')]
    
    # Procesar los datos
    data = []
    current_cluster = None
    
    for line in lines:
        # Saltar las líneas de encabezado
        if line.startswith('Cluster') or line.startswith('Cantidad'):
            continue
        
        # Verificar si es una nueva entrada de cluster
        if re.match(r'^\s*\d+\s+\d+', line):
            if current_cluster:  # Guardar el cluster anterior
                data.append(current_cluster)
            
            # Procesar nueva línea de cluster
            parts = re.split(r'\s{2,}', line.strip(), maxsplit=3)
            current_cluster = {
                'cluster': int(parts[0]),
                'cantidad_de_palabras_clave': int(parts[1]),
                'porcentaje_de_palabras_clave': float(parts[2].replace(',', '.').replace('%', '').strip()),
                'principales_palabras_clave': parts[3] if len(parts) > 3 else ''
            }
        elif current_cluster:  # Continuación de palabras clave
            current_cluster['principales_palabras_clave'] += ' ' + line.strip()
    
    # Añadir el último cluster
    if current_cluster:
        data.append(current_cluster)
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Función para limpiar palabras clave exactamente como en el test
    def clean_keywords(keywords):
        # Normalizar espacios
        cleaned = ' '.join(keywords.split())
        # Manejar comas específicamente
        cleaned = re.sub(r',\s*', ', ', cleaned)
        # Eliminar punto final si existe
        if cleaned.endswith('.'):
            cleaned = cleaned[:-1]
        # Eliminar coma final si existe
        if cleaned.endswith(','):
            cleaned = cleaned[:-1]
        return cleaned.strip()
    
    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(clean_keywords)
    
    # Ordenar por cluster y resetear índice
    df = df.sort_values('cluster').reset_index(drop=True)
    
    return df

print(pregunta_01())
