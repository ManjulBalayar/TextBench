"""
In this file, I will be utilizing BERT to generate tokens for my given input sequence + utilizing
the model that I've trained to generate sentiment analysis classification on the text input. The
model training is under the BERT_Reviews.ipynb file. 
"""

from transformers import AutoTokenizer
from transformers import BertModel
import torch
from torch import nn, optim
from torch.utils import data

BERT_MODEL = "bert-base-uncased"

def bert_tokenizer(text):
	tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
	tokens = tokenizer.tokenize(text)
	return tokens

class BERTSentimentClassifier(nn.Module):
	
	def __init__(self, n_classes):
		super(BERTSentimentClassifier, self).__init__()
		self.bert = BertModel.from_pretrained(BERT_MODEL)
		self.drop = nn.Dropout(p=0.30)
		self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
		self.softmax = nn.Softmax(dim=1)

	def forward(self, input_ids, attention_mask):
		outputs = self.bert(
			input_ids=input_ids,
			attention_mask=attention_mask,
		)
		pooled_output = outputs.pooler_output
		output = self.drop(pooled_output)
		output = self.out(output)
		return output

def bert_predict(text):
    class_names = ['negative', 'neutral', 'positive']
    model = BERTSentimentClassifier(len(class_names))
    model.load_state_dict(torch.load('models/bert-reviews.bin', map_location=torch.device('cpu')))

    model.eval()

    bert_tokenizer(text)
    print()

    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
    encoded_review = tokenizer.encode_plus(
        text,
        max_length=128,
        add_special_tokens=True,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors='pt'
    )

    input_ids = encoded_review['input_ids']
    attention_mask = encoded_review['attention_mask']

    with torch.inference_mode():
        output = model(input_ids, attention_mask)
        _, pred = torch.max(output, dim=1)
    
    return class_names[pred.item()]



