from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from datetime import datetime
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError
import os
import numpy as np

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno
DB_URI = os.getenv('DB_URI')
# Verificar que DB_URI no está vacío
if not DB_URI:
    raise ConfigurationError("DB_URI no está definido en el archivo .env")

# Configuración de Flask
app = Flask(__name__)
CORS(app)

# Cargar el modelo y el vectorizador entrenado
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

try:
    # Configuración de la base de datos y la API de YouTube usando variables de entorno
    client = MongoClient(DB_URI)
    # Verificar la conexión
    client.admin.command('ping')
    print("¡Conexión exitosa a MongoDB!")
    db = client.youtube_comments
except ConfigurationError as e:
    print(f"Error de configuración de MongoDB: {str(e)}")
    raise
except Exception as e:
    print(f"Error al conectar con MongoDB: {str(e)}")
    raise

# Clasificar un comentario
def classify_comment(comment):
    # Vectorizar el comentario
    vectorized_comment = vectorizer.transform([comment])
    
    # Predecir con el modelo SVM
    prediction = model.predict(vectorized_comment)
    
    # Convertir el resultado a un valor escalar
    prediction = prediction[0]
    
    # Mensaje basado en la predicción
    message = (
        "😱 El comentario contiene frases o palabras de odio."
        if prediction == "Negative"
        else "¡Buen comentario! 🥰 No es discurso de odio"
    )
    
    return {"comment": comment, "message": message, "prediction": prediction}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Obtener el comentario del formulario
        comment = request.form['analysis_comment']

        # Clasificar el comentario
        result = classify_comment(comment)

        # Preparar el documento para guardar en la base de datos
        document = {
            "comment": result['comment'],
            "prediction": result['prediction'],
            "timestamp": datetime.utcnow()
        }

        # Guardar en la base de datos MongoDB
        insert_result = db.comments.insert_one(document)

        # Confirmar que se insertó correctamente
        confirmation_message = (
            "El comentario fue guardado en la base de datos correctamente."
            if insert_result.inserted_id else "Error al guardar el comentario en la base de datos."
        )

        # Guardar en un archivo CSV
        csv_file = 'comments.csv'
        new_row = {
            "comment": result['comment'],
            "prediction": result['prediction'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Crear o actualizar el archivo CSV
        if not os.path.isfile(csv_file):
            df = pd.DataFrame([new_row])
            df.to_csv(csv_file, index=False)
        else:
            df = pd.DataFrame([new_row])
            df.to_csv(csv_file, mode='a', index=False, header=False)

        # Retornar JSON con los resultados
        return jsonify({
            "comment": result['comment'],
            "message": result['message'],
            "database_message": confirmation_message
        })
    except Exception as e:
        # En caso de error, retornar JSON con el mensaje de error
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)