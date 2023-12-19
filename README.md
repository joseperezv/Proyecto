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

Ejecuta el script `etl_functions.py` para obtener datos de la NASA, enviar alertas por correo y cargar datos en Redshift.

```bash
python etl_functions.py
```


## Personalización de Umbrales y Parámetros

Personaliza los umbrales de alerta y los parámetros de la API según tus necesidades.

### Dependencias

Asegúrate de tener las siguientes dependencias instaladas:

- `requests`
- `pandas`
- `smtplib`
- `psycopg2`

## Ejecución con Docker Compose

Este proyecto utiliza Docker Compose para simplificar la configuración y ejecución del entorno. Sigue estos pasos para ejecutar el proyecto utilizando Docker Compose:

 **Construir y Levantar los Contenedores**:

   ```bash
   docker-compose up --build
```

**Detener y Limpiar los Contenedores:

Cuando hayas terminado, puedes detener y limpiar los contenedores usando:

```bash
docker-compose down
```
Esto detendrá y eliminará los contenedores, pero conservará los datos de PostgreSQL en el volumen postgres-db-volume.

Asegúrate de tener Docker Compose instalado antes de seguir estos pasos.

> [!NOTE]
> Si necesitas personalizar alguna configuración específica, puedes hacerlo en el archivo docker-compose.yaml según tus necesidades.
   
## Integración con Apache Airflow

### Configuración de Airflow

#### Instalación de Apache Airflow

Asegúrate de tener Apache Airflow instalado. Puedes instalarlo con el siguiente comando:

```bash
pip install apache-airflow
```

## Configuración de Airflow
Configura tu archivo airflow.cfg. Encuentra este archivo en el directorio donde instalaste Airflow. Algunas configuraciones clave son:

- Conexión a Redshift: Asegúrate de tener la configuración correcta para conectarte a tu base de datos Redshift.

- Configuración de Correo Electrónico: Especifica las configuraciones necesarias para enviar correos electrónicos desde Airflow.

## Definición del DAG en Airflow
### Script Python del DAG
Crea un script Python que define tu DAG. Aquí proporcionas un ejemplo que utiliza las funciones get_asteroid_data y load_data_to_redshift. Asegúrate de configurar las variables necesarias como api_key, start_date, y end_date.

### Ubicación del Script
Coloca tu script Python en el directorio correcto de Airflow, por ejemplo, en el directorio dags.
            
### Ejecución de Airflow
Inicia el servicio de Airflow con el siguiente comando:

```bash
Copy code
airflow webserver --port 8080
```

Abre otro terminal y ejecuta:

```bash
Copy code
airflow scheduler
```

Ahora puedes acceder al panel de control de Airflow en http://localhost:8080 y ver y ejecutar tu DAG.

## Datos Clave
Asegúrate de configurar correctamente los siguientes datos clave:

- API Key de la NASA: Configura tu API key de la NASA en el script del DAG.

- Credenciales de Redshift: Proporciona las credenciales necesarias para conectarte a tu base de datos Redshift en la configuración de Airflow.

- Configuración de Correo Electrónico: Especifica las configuraciones correctas para que Airflow pueda enviar alertas por correo electrónico.
