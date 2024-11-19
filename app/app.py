import joblib
import pandas as pd
import datetime
from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.exceptions import DefaultCredentialsError
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from dotenv import load_dotenv
from scraping import get_comments_selenium
import os


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno
DB_URI = os.getenv('DB_URI')
API_KEY = os.getenv('API_KEY')

# Verificar que DB_URI no está vacío
if not DB_URI:
    raise ConfigurationError("DB_URI no está definido en el archivo .env")

# Configurar la aplicación Flask
app = Flask(__name__)

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    # Cargar el modelo y vectorizador
    model = joblib.load(os.path.join(BASE_DIR, 'models', 'svm_model.pkl'))
    vectorizer = joblib.load(os.path.join(BASE_DIR, 'models', 'vectorizer.pkl'))
    print("Modelo y vectorizador cargados exitosamente")
          
    # Configuración de la base de datos y la API de YouTube usando variables de entorno
    client = MongoClient(DB_URI)
    # Verificar la conexión
    client.admin.command('ping')
    print("¡Conexión exitosa a MongoDB!")
    db = client.youtube_comments
    try:
    # Verificar que la API_KEY existe
        if not API_KEY:
            raise ValueError("API_KEY no está definida en el archivo .env")
        
        # Crear el servicio de YouTube
        youtube = build(
            'youtube', 
            'v3', 
            developerKey=API_KEY,
            static_discovery=False  # Añade este parámetro
        )
        print("Cliente de YouTube configurado exitosamente")
        
    except ValueError as e:
        print(f"Error con la API key: {str(e)}")
        raise
    except Exception as e:
        print(f"Error al configurar el cliente de YouTube: {str(e)}")
        raise

except ConfigurationError as e:
    print(f"Error de configuración de MongoDB: {str(e)}")
    raise
except Exception as e:
    print(f"Error al conectar con MongoDB: {str(e)}")
    raise

# Función para extraer comentarios de un video de YouTube
def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        textFormat='plainText'
    )
    response = request.execute()

    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    return comments


# Después de cargar las variables de entorno
print(f"DB_URI está definido: {'Sí' if DB_URI else 'No'}")
if DB_URI:
    # Ocultar la contraseña si existe
    safe_uri = DB_URI.replace('//:' if '//:' in DB_URI else '//', '//***:***@')
    print(f"DB_URI format: {safe_uri}")

def predict_comment(comment):
    """
    Utiliza el modelo y el vectorizador cargados para predecir si un comentario contiene odio.
    Retorna 1 para odio y 0 para no odio.
    """
    print(f"Comentario recibido para predecir: {comment}")  
    # Transformar el comentario en la representación TF-IDF
    X = vectorizer.transform([comment])
    print(f"Representación TF-IDF: {X}")

    # Hacer la predicción con el modelo cargado
    try:
        prediction = model.predict(X)[0]
        print(f"Predicción: {prediction}")  # Verifica la predicción
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        prediction = None
    
    return prediction

# Función para clasificar comentarios
def classify_comments(comments):
    comments_df = pd.DataFrame(comments, columns=['comment'])
    X = vectorizer.transform(comments_df['comment'])
    predictions = model.predict(X)
    comments_df['prediction'] = predictions
    return comments_df

# Función para guardar los resultados en la base de datos
def save_to_db(df, video_id):
    data = df.to_dict('records')
    for item in data:
        item['video_id'] = video_id
        item['timestamp'] = datetime.datetime.now()
    db.comments.insert_many(data)

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form['video_url']
    comments = get_comments_selenium(video_url, max_comments=10)

    if not comments:
        return jsonify({'message': 'No se encontraron comentarios o hubo un error'}), 404

    results = []
    for comment in comments:
        prediction = predict_comment(comment)
        # Verifica si la predicción es válida antes de generar el resultado
        if prediction is None:
            result_text = "Hubo un error al procesar el comentario."
        elif prediction == 1:
            result_text = "El comentario contiene frases o palabras de odio."
        else:
            result_text = "Comentario más amable!"
        # Guardar en MongoDB
        db.comments.insert_one({
            "video_id": video_url.split('=')[-1],
            "comment": comment,
            "prediction": prediction,
            "timestamp": datetime.datetime.utcnow()
        })
        
        results.append({
            "comment": comment,
            "result": result_text
        })
    print(results)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
