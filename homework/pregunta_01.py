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

    # Leer el archivo como texto plano
    with open('./files/input/clusters_report.txt', 'r', encoding='utf-8') as file:
        #lines = file.readlines()
        lines = [line.strip() for line in file.readlines() if line.strip()]

    # Construcción de encabezados con base en las dos primeras líneas
    header1 = re.split(r'\s{2,}', lines[0])
    header2 = re.split(r'\s{2,}', lines[1])

    # Construir encabezados combinados y separados por guiones bajos
    headers = [
        header1[0],  # Cluster
        f"{header1[1]} {header2[0]}".strip(),
        f"{header1[2]} {header2[1]}".strip(),
        header1[3]
    ]
    # Limpiar nombres de columnas
    headers = [header.lower().replace(' ', '_') for header in headers]

    # Procesar las líneas para extraer datos
    data = []
    current_cluster = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Ignorar líneas vacías
        
        # Detectar líneas de cluster (ej: "1     105             15,9 % ...")
        if re.match(r'^\s*\d+\s+\d+', line):
            parts = re.split(r'\s{2,}', line, maxsplit=3)  # Dividir en 4 partes
            if len(parts) >= 4:
                current_cluster = {
                    headers[0]: parts[0].strip(),
                    headers[1]: parts[1].strip(),
                    headers[2]: parts[2].strip(),
                    headers[3]: parts[3].strip()
                }
                data.append(current_cluster)
        elif current_cluster:  # Continuación de palabras clave
            current_cluster[headers[3]] += ' ' + line.strip()

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Limpiar espacios adicionales en palabras clave
    df[headers[3]] = df[headers[3]].str.replace(r'\s+', ' ', regex=True)

    # Convertir a enteros los datos de las columnas 0 y 1
    df[headers[0]] = df[headers[0]].astype(int)
    df[headers[1]] = df[headers[1]].str.replace(',', '').astype(int)
    df[headers[2]] = df[headers[2]].str.replace('%', '').str.replace(',', '.').astype(float)

    # Mostrar el DataFrame
    print(df.head())

print(pregunta_01())
