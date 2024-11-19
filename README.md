# Detectando Mensajes de Odio en YouTube

Este proyecto tiene como objetivo crear una solución que detecte automáticamente los mensajes de odio en los comentarios de YouTube, utilizando técnicas de procesamiento de lenguaje natural (NLP) y machine learning.

## Descripción

YouTube ha solicitado una solución automatizada para identificar mensajes de odio en los comentarios de sus videos. Para ello, hemos desarrollado un modelo de **Machine Learning** capaz de clasificar comentarios como "de odio" o "no de odio". La solución se ha escalado a través de una API que permite analizar los comentarios en tiempo real.

## Tecnologías

- **Python**: Lenguaje de programación principal.
- **NLTK**: Librería de NLP para preprocesamiento de texto.
- **scikit-learn**: Modelos de ML y herramientas de validación.
- **Flask**: Framework para la creación de la API.
- **Base de datos**: MongoDB para guardar los comentarios y sus predicciones.

## Instrucciones de Uso

## Requisitos Previos**

Antes de ejecutar el proyecto, asegúrate de contar con lo siguiente:

- **Python 3.7 o superior** instalado en tu sistema.
- **Clave API de YouTube Data API v3:** Necesaria para utilizar la función que extrae comentarios de videos de YouTube.  
  > Puedes solicitar tu clave API en [Google Cloud Console](https://console.cloud.google.com/). 
- **ChromeDriver**: Instalado y compatible con tu versión de Google Chrome, necesario para la función de scraping con Selenium. 

---
## **1. Crear y Configurar el Entorno**

### **Crea un entorno virtual (opcional pero recomendado):**

```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

### **Instalar dependencias**
pip install -r requirements.txt


### **Clonar el Repositorio**

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/AI-School-F5-P3/NLPL2-YUTU.git
cd NLPL2-YUTU

### **Crea un archivo .env en la raíz del proyecto con las siguientes variables de entorno:**

API_KEY=TU_CLAVE_API_YOUTUBE

### **Ejecución**
Inicia la aplicación Flask ejecutando el siguiente comando en tu CLI

python app.py

La aplicación estará disponible en:
http://127.0.0.1:5000/


###  **Uso Desde la Plataforma Web**

Abre tu navegador y accede a: http://127.0.0.1:5000/.

Opciones disponibles:

Ingresar un comentario: Escribe un comentario en el cuadro de texto y presiona el botón Analizar. Verás el resultado del análisis en pantalla.

Ingresar un enlace de video: Proporciona la URL de un video de YouTube y presiona Obtener comentarios. La aplicación extraerá los comentarios del video y los analizará automáticamente.

Nota: Debes contar con una clave válida de la API de YouTube para usar esta funcionalidad. Solicítala en Google Cloud Console.

Observa los resultados directamente en la página.



