# 🚨 Detectando Mensajes de Odio en YouTube 🔍

Este proyecto tiene como objetivo crear una solución que detecte automáticamente los mensajes de odio en los comentarios de YouTube, utilizando técnicas de procesamiento de lenguaje natural (NLP) y machine learning.

## 📝 Descripción

YouTube ha solicitado una solución automatizada para identificar mensajes de odio en los comentarios de sus videos. Para ello, hemos desarrollado un modelo de **Machine Learning** capaz de clasificar comentarios como "de odio" o "no de odio". La solución se ha escalado a través de una API que permite analizar los comentarios en tiempo real.

## 🛠 Tecnologías

- **Python**: Lenguaje de programación principal 🐍
- **NLTK**: Librería de NLP para preprocesamiento de texto 📊
- **scikit-learn**: Modelos de ML y herramientas de validación 🤖
- **Flask**: Framework para la creación de la API 🌐
- **Bootstrap, CSS y HTML**:Para la interfaz
- **MongoDB**: Base de datos para guardar comentarios y predicciones 💾

## 🚀 Instrucciones de Uso

### 📋 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de contar con:

- **Python 3.7 o superior** instalado 🐍
- **Clave API de YouTube Data API v3** 🔑
 > Puedes solicitar tu clave API en [Google Cloud Console](https://console.cloud.google.com/)
- **ChromeDriver** compatible con tu versión de Google Chrome 🌐

### 🔧 Configuración del Entorno

1. **Crear entorno virtual**:

python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

### Instalar dependencias:

pip install -r requirements.txt

### Clonar repositorio:

git clone https://github.com/AI-School-F5-P3/NLPL2-YUTU.git
cd NLPL2-YUTU

## Configurar variables de entorno:
Crea un archivo .env con:

API_KEY=TU_CLAVE_API_YOUTUBE

### 🖥 Ejecución
Inicia la aplicación Flask:
python app.py

La aplicación estará disponible en: http://127.0.0.1:5000/

### 🌍 Uso en la Plataforma Web

Abre tu navegador en: http://127.0.0.1:5000/
Opciones:

Analizar un comentario individual
Obtener comentarios de un video de YouTube



## ⚠️ Nota: Requiere clave API de YouTube válida.

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Por favor, lee las guías de contribución antes de enviar un pull request.

## Links de la presentaciòn y espacio de trabajo

canva:
https://www.canva.com/design/DAGW1d7pzp4/dGlLRsgDn157y_HR5vbiaw/edit?utm_content=DAGW1d7pzp4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


Trello:
https://trello.com/invite/b/6731e945aef605c25c9d3da8/ATTI99556f4999363da67811018b1ae0adaa05D601BE/youtube-project-ml
