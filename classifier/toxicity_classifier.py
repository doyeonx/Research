import sys
sys.path.insert(1, '../')
import files
import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset
import numpy as np

TOXICITY_DESCRIPTION = {
    "Insulting": "Using derogatory language to demean others.",
    "Entitled": "Expressing a sense of superiority and demanding behavior.",
    "Arrogant": "Displaying an overbearing sense of self-importance.",
    "Trolling": "Provoking others intentionally to create discord.",
    "Unprofessional": "Engaging in behavior that is not aligned with professional conduct."
}

def tokenize_comments(comments):
    inputs = tokenizer(
        comments,
        return_tensors='pt',
        max_length=512,
        truncation=True,
        padding=True
    )
    return inputs

def classify_comment(post):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([post])

def main():
    json_files = files.JSON_FILES
    
    # for i in range(len(json_files)):
    #     file_name = json_files[i]['file_name']
    #
    #     with open(file_name, 'r') as f:
    #         file = json.load(f)
    
    input_file_name = '../data/test_data.json'

    with open(input_file_name, 'r') as f:
        input_file = json.load(f)

    model_name = "unitary/toxic-bert"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)

main()
