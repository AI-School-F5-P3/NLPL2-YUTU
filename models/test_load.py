import os
print("Archivos en models/:", os.listdir('models'))

import joblib

try:
    model = joblib.load('models/svm_model.pkl')
    vectorizer = joblib.load('models/vectorizer.pkl')
    
    # Probar el modelo
    texto_prueba = ["Este es un comentario de prueba"]
    X = vectorizer.transform(texto_prueba)
    prediccion = model.predict(X)
    print("Predicción:", "ODIO" if prediccion[0] == 1 else "NO ODIO")
    print("¡Modelo cargado y probado exitosamente!")
except Exception as e:
    print(f"Error: {str(e)}")