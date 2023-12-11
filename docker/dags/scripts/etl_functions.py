
import requests
import pandas as pd


api_key = 'vaJwtaRz3N8gCPfOQeh9rOtjRJvchtNyRyvPMZEl'
start_date = '2023-10-10'
end_date = '2023-10-17'

def get_asteroid_data(api_key, start_date, end_date):
    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'

    response = requests.get(url)
    data = response.json()

    if 'near_earth_objects' in data:
        asteroids = data['near_earth_objects']

        asteroid_data = []

        for date in asteroids:
            for asteroid in asteroids[date]:
                asteroid_info = {
                    "Nombre": asteroid['name'],
                    "Fecha de aproximación más cercana": date,
                    "Diámetro estimado (metros)": asteroid['estimated_diameter']['meters']['estimated_diameter_min'],
                    "Distancia a la Tierra (kilómetros)": asteroid['close_approach_data'][0]['miss_distance']['kilometers']
                }
                asteroid_data.append(asteroid_info)

        print("Conexion exitosa")
        return pd.DataFrame(asteroid_data)
    else:
        print("La solicitud a la API falló.")
        return None

get_asteroid_data(api_key, start_date, end_date)




import psycopg2
redshift_credentials = {
    'user': 'joseperezv65_coderhouse',
    'password': '1w180Ap2WA',
    'host': 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
    'port': 5439,
    'database': 'data-engineer-database'
}

df = get_asteroid_data(api_key='vaJwtaRz3N8gCPfOQeh9rOtjRJvchtNyRyvPMZEl', start_date='2023-10-10', end_date='2023-10-17')

def load_data_to_redshift(df, redshift_credentials):
    if df is not None:
        try:
            conn = psycopg2.connect(
                user=redshift_credentials['user'],
                password=redshift_credentials['password'],
                host=redshift_credentials['host'],
                port=redshift_credentials['port'],
                database=redshift_credentials['database']
            )

            cursor = conn.cursor()

            for index, row in df.iterrows():
                cursor.execute(
                    "SELECT 1 FROM asteroid_data WHERE Nombre = %s LIMIT 1;",
                    (row['Nombre'],)
                )
                existing_record = cursor.fetchone()

                if existing_record is None:
                    cursor.execute(
                        f"INSERT INTO asteroid_data (Nombre, Fecha_de_aproximacion_mas_cercana, Diametro_estimado_metros, Distancia_a_la_Tierra_kilometros) VALUES (%s, %s, %s, %s);",
                        (row['Nombre'], row['Fecha de aproximación más cercana'], row['Diámetro estimado (metros)'], row['Distancia a la Tierra (kilómetros)'])
                    )
                else:
                    print(f"Asteroide '{row['Nombre']}' ya existe en la tabla, no se insertó duplicado.")

            conn.commit()
            cursor.close()
            conn.close()
            print("Los datos se han cargado correctamente en la tabla en Redshift.")
        except Exception as e:
            print("Error al cargar datos en Redshift:", str(e))

load_data_to_redshift(df, redshift_credentials)