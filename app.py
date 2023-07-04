from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello from the backend!'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']

    # Perform predictive text completion using python implementation

    # Dummy example: Appending ' world' to the input text
    
    predicted_text = text + ' world'

    return jsonify({'predictedText': predicted_text})

if __name__ == '__main__':
    print("running!")
    app.run(port=8000)