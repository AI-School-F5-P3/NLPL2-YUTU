from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from datetime import datetime
from flask_cors import CORS



# Configuración de Flask
app = Flask(__name__)
CORS(app)
# Cargar el modelo y el vectorizador entrenado
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Clasificar un comentario
def classify_comment(comment):
  
    # Vectorizar el comentario
    vectorized_comment = vectorizer.transform([comment])
    
    # Predecir con el modelo SVM
    prediction = model.predict(vectorized_comment)
    
    # Mensaje basado en la predicción
    message = "El comentario contiene frases o palabras de odio." if prediction[0] == 'Negative' else "¡Qué comentario más amable! No es discurso de odio"
    
    return {"comment": comment, "message": message}

# Rutas de la aplicación Flask
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
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
