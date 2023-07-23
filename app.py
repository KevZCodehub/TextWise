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

@app.route('/next-word-predict', methods=['POST'])
def next_word_predict():
    data = request.get_json()
    text = data['text']

    # Tokenize the input text
    input_ids = tokenizer.encode(text, return_tensors='pt')

    # Generate next word prediction
    outputs = model.generate(input_ids, max_length=100, num_return_sequences=1, temperature=0.7)

    # Decode and format the predicted text
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Find the index of the space character after the input text ends
    index = predicted_text.find(text) + len(text) + 1
    if index != -1:
        # Truncate the predicted text up to the next word
        next_word_index = predicted_text.find(" ", index)
        if next_word_index != -1:
            predicted_text = predicted_text[:next_word_index]

    return jsonify({'predictedText': predicted_text})

@app.route('/next-sentence-predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']

    # Tokenize the input text
    input_ids = tokenizer.encode(text, return_tensors='pt')

    # Generate text predictions
    outputs = model.generate(input_ids, max_length=50, num_return_sequences=1, temperature=0.7)

    # Decode and format the predicted text
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Cut off the text at the next sentence
    next_sentence_index = find_next_sentence_index(predicted_text)

    # Determine the final cutoff index
    if next_sentence_index != -1:
        cutoff_index = next_sentence_index
    else:
        cutoff_index = len(predicted_text)

    # Cut off the text at the determined index
    predicted_text = predicted_text[:cutoff_index]

    return jsonify({'predictedText': predicted_text})

def find_next_sentence_index(text):
    sentence_endings = [". ", "? ", "! "]
    min_index = -1
    for ending in sentence_endings:
        index = text.find(ending)
        if index != -1 and (min_index == -1 or index < min_index):
            min_index = index
    return min_index

if __name__ == '__main__':
    print("running!")
    app.run(port=8000)
