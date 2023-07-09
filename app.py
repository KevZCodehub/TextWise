from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2TokenizerFast, GPT2LMHeadModel

app = Flask(__name__)
CORS(app)

# Load pre-trained GPT-2 model and tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

@app.route('/', methods=['GET'])
def hello():
    return 'Hello from the backend!'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']

    # Tokenize the input text
    input_ids = tokenizer.encode(text, return_tensors='pt')

    # Generate text predictions
    outputs = model.generate(input_ids, max_length=50, num_return_sequences=1, temperature=0.7)

    # Decode and format the predicted text
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'predictedText': predicted_text})

if __name__ == '__main__':
    print("running!")
    app.run(port=8000)