import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load the descriptions of toxicity types from the paper
url = "https://cmustrudel.github.io/papers/osstoxicity22.pdf"
response = requests.get(url)
paper_content = response.content

# Dummy descriptions for simplification (replace with actual descriptions extracted from the paper)
toxicity_descriptions = {
    "Insulting": "Using derogatory language to demean others.",
    "Entitled": "Expressing a sense of superiority and demanding behavior.",
    "Arrogant": "Displaying an overbearing sense of self-importance.",
    "Trolling": "Provoking others intentionally to create discord.",
    "Unprofessional": "Engaging in behavior that is not aligned with professional conduct."
}

# Load the JSON file containing toxic comments
input_file = 'toxic_comments.json'
output_file = 'classified_toxic_comments.json'

with open(input_file, 'r') as f:
    comments = json.load(f)

# Function to classify comments based on descriptions
def classify_comment(comment, context):
    combined_text = comment + " " + context
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([combined_text] + list(toxicity_descriptions.values()))
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
    labels = kmeans.labels_
    return list(toxicity_descriptions.keys())[labels[0]]

# Classify each comment
classified_comments = []
for comment in comments:
    classified_comments.append({
        "comment": comment['comment'],
        "context": comment['context'],
        "type": classify_comment(comment['comment'], comment['context'])
    })

# Write the classified comments to the output JSON file
with open(output_file, 'w') as f:
    json.dump(classified_comments, f, indent=4)

print(f"Classified comments saved to {output_file}")
