# Proyecto de Monitoreo de Asteroides

Este proyecto tiene como objetivo realizar un monitoreo de asteroides que se acercan a la Tierra y alertar sobre aquellos que cumplen ciertos umbrales de diámetro estimado y distancia a la Tierra.

## Funcionalidades Principales

1. **Obtención de Datos de la NASA**: Utiliza la API de la NASA para obtener datos sobre asteroides que se aproximan a la Tierra en un rango de fechas determinado.

2. **Alertas por Correo Electrónico**: Envía alertas por correo electrónico cuando un asteroide tiene un diámetro estimado superior a cierto umbral o se acerca a la Tierra a una distancia mayor que otro umbral.

3. **Almacenamiento en Redshift**: Carga los datos relevantes de los asteroides en una base de datos Redshift para su posterior análisis.

## Configuración

1. **API Key de la NASA**: Reemplaza el valor de `api_key` en el código con tu propia API key de la NASA.

2. **Credenciales de Correo Electrónico**: Configura el servidor SMTP y las credenciales de tu correo electrónico para poder enviar alertas por correo.

3. **Credenciales de Redshift**: Proporciona las credenciales necesarias para conectarte a tu base de datos Redshift.

## Uso

1. Ejecuta el script `etl_functions.py` para obtener datos de la NASA, enviar alertas por correo y cargar datos en Redshift.

   ```bash
   python etl_functions.py

2. Personaliza los umbrales de alerta y los parámetros de la API según tus necesidades.
Dependencias:
requests
pandas
smtplib
psycopg2
