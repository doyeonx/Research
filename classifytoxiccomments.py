import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Define the file paths
input_file = 'comments.json'
output_file = 'toxic_comments.json'

# Load the JSON file containing comments and context
with open(input_file, 'r') as f:
    comments = json.load(f)

# Load the pre-trained BERT model and tokenizer for toxicity classification
model_name = 'unitary/toxic-bert'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Function to classify the comment and get toxicity score
def classify_comment(comment):
    inputs = tokenizer(comment, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
    toxicity_score = scores[0][1].item()  # Assuming class 1 is toxic
    return toxicity_score

# Classify each comment and save toxic comments
toxic_comments = []
for comment in comments:
    comment_text = comment['comment']
    context_text = comment['context']
    toxicity_score = classify_comment(comment_text)
    
    if toxicity_score > 0.5:  # Assuming a threshold of 0.5 for toxicity
        toxic_comments.append({
            "comment": comment_text,
            "context": context_text,
            "toxicity_score": toxicity_score
        })

# Write the toxic comments to the output JSON file
with open(output_file, 'w') as f:
    json.dump(toxic_comments, f, indent=4)

print(f"Toxic comments saved to {output_file}")