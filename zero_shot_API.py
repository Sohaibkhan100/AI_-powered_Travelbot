
from flask import Flask, request, jsonify
import spacy
from transformers import pipeline
from langdetect import detect
from deep_translator import GoogleTranslator

app = Flask(__name__)

nlp = spacy.load("en_core_web_trf")  
intent_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

possible_intents = ["hotel_search", "flight_search", "transfers", "tours", "combined_search"]
intent_threshold = 0.4  
def process_query(query):
    try:
        detected_lang = detect(query)
        print(f"Detected Language: {detected_lang}")

        if detected_lang != 'en':
            try:
                translated_query = GoogleTranslator(source=detected_lang, target='en').translate(query)
                print(f"Translated Query: {translated_query}")
            except Exception as e:
                print(f"Translation Error: {e}")
                translated_query = query  
        else:
            translated_query = query

        intent_result = intent_model(translated_query, candidate_labels=possible_intents)
        scores = {label: score for label, score in zip(intent_result["labels"], intent_result["scores"])}

        flight_confidence = scores.get("flight_search", 0)
        hotel_confidence = scores.get("hotel_search", 0)
        transfers_confidence = scores.get("transfers", 0)

        if flight_confidence > intent_threshold and hotel_confidence > intent_threshold:
            predicted_intent = "combined_search"
        elif max(scores.values()) > intent_threshold:
            predicted_intent = max(scores, key=scores.get)
        else:
            predicted_intent = "unknown"

        doc = nlp(translated_query)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        ner_dict = {
            'budget': [],
            'dates': [],
            'locations': [],
            'time': [],
            'money': []
        }

        for ent_text, ent_label in entities:
            if ent_label == 'MONEY':
                ner_dict['money'].append(ent_text)
            elif ent_label == 'DATE':
                ner_dict['dates'].append(ent_text)
            elif ent_label == 'GPE': 
                ner_dict['locations'].append(ent_text)
            elif ent_label == 'TIME':
                ner_dict['time'].append(ent_text)

        ner_dict['budget'] = []
        for money_text in ner_dict['money']:
            try:
                values = money_text.replace('$', '').split(' to ')
                ner_dict['budget'].extend([int(value) for value in values if value.isdigit()])
            except Exception as e:
                print(f"Error parsing budget values: {e}")

        response_url = f"https://www.test.com?querytype={predicted_intent}&budget={ner_dict['budget']}&dates={ner_dict['dates']}&locations={ner_dict['locations']}&time={ner_dict['time']}"

        result = {
            "Predicted Intent": predicted_intent,
            "Confidence Scores": scores,
            "Extracted Entities": ner_dict,
            "URL": response_url
        }

        print(f"Query: {query}")
        print(f"Predicted Intent: {predicted_intent}")
        print(f"Confidence Scores: {scores}")
        print(f"Extracted Entities: {ner_dict}\n")
        print(f"Generated URL: {response_url}\n")

        return result

    except Exception as e:
        print(f"Processing Error: {e}")
        return {"error": str(e)}

@app.route('/process_query', methods=['POST'])
def api_process_query():
    try:
        data = request.get_json()
        query = data.get("query")

        result = process_query(query)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
