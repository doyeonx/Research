import json
import torch
import csv
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from lime.lime_text import LimeTextExplainer

# Load a more advanced pre-trained BERT model for toxicity classification
model_name = "microsoft/deberta-v3-large"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Load the JSON data
with open('../data/forum/test_data.json', 'r') as json_file:
    forum_data = json.load(json_file)

# Initialize the classification pipeline
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer, return_all_scores=True)

# Initialize LIME explainer
explainer = LimeTextExplainer(class_names=['non-toxic', 'toxic'])

def get_toxicity_scores(comment):
    results = classifier(comment)
    for result in results[0]:
        if result['label'] == 'LABEL_1':  # Assuming 'LABEL_1' is toxic
            return result['score']
    return 0.0

def explain_toxicity(comment):
    exp = explainer.explain_instance(comment, classifier, num_features=6)
    return exp.as_list()

# Process each comment in the forum data
toxic_comments = []

for post in forum_data:
    for comment in post['comments']:
        if 'content' in comment:
            score = get_toxicity_scores(comment['content'])
            # Consider a comment toxic if the score is above a certain threshold
            threshold = 0.1
            if score >= threshold:
                explanation = explain_toxicity(comment['content'])
                toxic_comments.append({
                    "comment": comment['content'],
                    "toxicity_score": score,
                    "explanation": explanation
                })

# Save the toxic comments to a CSV file
csv_file_path = '../data/toxic_comments.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['comment', 'toxicity_score', 'explanation']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for toxic_comment in toxic_comments:
        writer.writerow({
            "comment": toxic_comment["comment"],
            "toxicity_score": toxic_comment["toxicity_score"],
            "explanation": ' | '.join([f"{feature}: {weight:.2f}" for feature, weight in toxic_comment["explanation"]])
        })

print(f"Toxic comments have been saved to {csv_file_path}")
