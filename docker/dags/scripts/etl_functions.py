import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import psycopg2

api_key = 'vaJwtaRz3N8gCPfOQeh9rOtjRJvchtNyRyvPMZEl'
start_date = '2023-10-10'
end_date = '2023-10-17'

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'joseperezv65@gmail.com'
smtp_password = 'bzyu txgy umvd belo'
sender_email = 'joseperezv65@gmail.com'
receiver_email = 'alvaherra@gmail.com'

# Thresholds para las alertas
diameter_threshold = 100  # Diámetro estimado en metros
distance_threshold = 500000  # Distancia a la Tierra en kilómetros

def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    body_html = MIMEText(body, 'html')
    message.attach(body_html)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

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
        df = pd.DataFrame(asteroid_data)

        df['Distancia a la Tierra (kilómetros)'] = pd.to_numeric(df['Distancia a la Tierra (kilómetros)'], errors='coerce')

        alert_table = "<table border='1'><tr><th>Nombre</th><th>Fecha de aproximación más cercana</th><th>Diámetro estimado (metros)</th><th>Distancia a la Tierra (kilómetros)</th></tr>"
        for index, row in df.iterrows():

            if pd.notna(row['Distancia a la Tierra (kilómetros)']):
                distancia_tierra = int(row['Distancia a la Tierra (kilómetros)'])

                if row['Diámetro estimado (metros)'] > diameter_threshold or distancia_tierra > distance_threshold:
                    alert_table += f"<tr><td>{row['Nombre']}</td><td>{row['Fecha de aproximación más cercana']}</td><td>{row['Diámetro estimado (metros)']}</td><td>{row['Distancia a la Tierra (kilómetros)']}</td></tr>"

        alert_table += "</table>"

        if alert_table != "<table border='1'><tr><th>Nombre</th><th>Fecha de aproximación más cercana</th><th>Diámetro estimado (metros)</th><th>Distancia a la Tierra (kilómetros)</th></tr></table>":
           
            send_email("Alertas de Asteroides", alert_table)

    else:
        print("La solicitud a la API falló.")
        df = None

    return df

df = get_asteroid_data(api_key, start_date, end_date)

import psycopg2
redshift_credentials = {
    'user': 'joseperezv65_coderhouse',
    'password': '1w180Ap2WA',
    'host': 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
    'port': 5439,
    'database': 'data-engineer-database'
}

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
