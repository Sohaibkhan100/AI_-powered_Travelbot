
import spacy
from transformers import pipeline
from langdetect import detect
from deep_translator import GoogleTranslator

nlp = spacy.load("en_core_web_trf")

intent_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

possible_intents = ["hotel search", "flight search", "transfers", "tours", "combined search"]
intent_threshold = 0.25

queries = [
    "Reserve a hotel room in Paris from 7th January 2025 to 10th January 2025, with a budget of $150 to $250 per night, arriving at 3 PM."
    # "Book a flight from New York to Paris between 10 PM on 5th December 2024 and 10th December 2024 for $300 to $400.",  # English
    # "Réservez un transfert de l'aéroport à mon hôtel le 6 décembre.",  # French
    # "Reserva un traslado desde el aeropuerto a mi hotel el 6 de diciembre.",  # Spanish
    # "ديسمبر 6 کو ہوٹل سے ایئرپورٹ تک منتقلی کی بکنگ کریں"  # Urdu
]

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

        predicted_intent = (
            "combined search" 
            if scores.get("flight search", 0) > intent_threshold and scores.get("hotel search", 0) > intent_threshold
            else max(scores, key=scores.get) if max(scores.values()) > intent_threshold 
            else "unknown"
        )

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

        print(f"Query: {query}")
        print(f"Predicted Intent: {predicted_intent}")
        print(f"Confidence Scores: {scores}")
        print(f"Extracted Entities: {ner_dict}\n")
        print("https://www.test.com"+f"?querytype={predicted_intent}&budget={ ner_dict['budget']}&dates={ner_dict['dates']}&locations={ner_dict['locations']}time={ner_dict['time']}")

        if detected_lang != 'en':
            try:
                response_text = f"Predicted Intent: {predicted_intent}, Entities: {ner_dict}"
                translated_response = GoogleTranslator(source='en', target=detected_lang).translate(response_text)
                print(f"Translated Response: {translated_response}\n")
            except Exception as e:
                print(f"Response Translation Error: {e}")

    except Exception as e:
        print(f"Processing Error: {e}")

for query in queries:
    process_query(query)
