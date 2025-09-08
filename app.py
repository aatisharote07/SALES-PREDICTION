from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from pathlib import Path

app = Flask(__name__)

PROJECT_DIR = Path(__file__).resolve().parent

# Lazy-load model and encoders, handle absence gracefully
model = None
encoders = None

def load_artifacts():
    global model, encoders
    model_path = PROJECT_DIR / 'random_forest_model.pkl'
    encoders_path = PROJECT_DIR / 'encoders.joblib'
    if model is None and model_path.exists():
        model = joblib.load(model_path)
    if encoders is None and encoders_path.exists():
        encoders = joblib.load(encoders_path)

@app.route('/')
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    load_artifacts()
    if model is None:
        return jsonify({'error': 'Model not found. Train the model first.'}), 503
    if encoders is None:
        return jsonify({'error': 'Encoders not found. Train the model first.'}), 503

    outlet_establishment_year = int(request.form['outlet_establishment_year'])
    outlet_size = request.form['outlet_size']
    outlet_location_type = request.form['outlet_location_type']
    outlet_type = request.form['outlet_type']

    try:
        input_data = pd.DataFrame({
            'Outlet_Size': [encoders['Outlet_Size'].transform([outlet_size])[0]],
            'Outlet_Location_Type': [encoders['Outlet_Location_Type'].transform([outlet_location_type])[0]],
            'Outlet_Type': [encoders['Outlet_Type'].transform([outlet_type])[0]],
            'Outlet_Age': [2024 - outlet_establishment_year]
        })
    except Exception as e:
        return jsonify({'error': f'Encoding error: {str(e)}'}), 400

    try:
        prediction = model.predict(input_data)
        return jsonify({'prediction': float(prediction[0])})
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    load_artifacts()
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'encoders_loaded': encoders is not None
    })

@app.route('/metadata', methods=['GET'])
def metadata():
    load_artifacts()
    result = {'encoders_loaded': encoders is not None}
    if encoders is not None:
        def classes_for(name):
            encoder = encoders.get(name)
            if encoder is None:
                return []
            # Return original class labels in encoder's learned order
            return [str(c) for c in encoder.inverse_transform(list(range(len(encoder.classes_))))]

        result.update({
            'Outlet_Size': classes_for('Outlet_Size'),
            'Outlet_Location_Type': classes_for('Outlet_Location_Type'),
            'Outlet_Type': classes_for('Outlet_Type')
        })
    return jsonify(result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
