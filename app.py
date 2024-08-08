from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load your trained machine learning model and scaler
model = joblib.load('model/new_model_saved.pkl')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict(flat=True)
    
    # Convert form data to DataFrame
    input_data = pd.DataFrame([data])
    
         
    
    
    # Perform prediction
    prediction = model.predict(input_data)[0]
    
    return jsonify({
        'message': 'Prediction successful',
        'predicted_bill': prediction
    })

if __name__ == '__main__':
    app.run(debug=True)

