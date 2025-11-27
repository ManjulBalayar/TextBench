"""
This file will be the rule-based layer where I will take the text and perform the following:
- Stopwords & a tokenization with naive approach without using external libraries. It will be lowercase + strip any punctuations + dropping stopwords.
- Regex patten extraction: Things like names, dates, etc. Main thing is utilizing and learning the `re` library in Python.
= Simple rule-based sentiment & topics: Get keywords maybe, positive or negative lexicons. 
"""

import re

STOP_WORDS = {
    # Articles
    "a", "an", "the",
    
    # Pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    
    # Prepositions
    "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below",
    "to", "from", "up", "down", "of", "off", "over", "under",
    
    # Conjunctions
    "and", "but", "or", "nor", "so", "yet", "because", "as", "if",
    "when", "where", "while", "although", "though", "unless", "until",
    
    # Common verbs
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "will", "would", "should", "could", "may", "might", "must", "can",
    
    # Question words
    "what", "which", "who", "whom", "whose", "why", "how",
    
    # Other common words
    "this", "that", "these", "those", "there", "here",
    "all", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "not", "only", "own", "same", "than", "too", "very",
    "just", "now", "then", "once", "also", "again", "further",
    "any", "every", "either", "neither", "another",
    "out", "such", "via"
}

STOP_WORDS_SET = set(STOP_WORDS)

def remove_punctuations(text):
	translator = str.maketrans({
                "!":"", ".":"", "?":"", 
                "#":"", "$":"", "%":"", 
                "&":"", ",":"", ":":"", 
                ";":"", "\"":"", "[":"",
                "]":"", "{":"", "}":"",
                "(":"", ")":"", "-":" ",
                "_":"", "=":"", "+":"",
                "*":"", "/":"", "\\":"",
                "|":"", "<":"", ">":"",
                "~":"", "`":"", "@":"",
                "^":"", "“": "", "”": "",
		 "’": "'",})	
	cleaned_text = text.translate(translator)
	return cleaned_text

def remove_stopwords(text):
	# 1. Lower case
	# 2. Remove punctuatiosn smartly, 'hello,' -> 'hello' but for 'it's' keep it as it is.
	# 3. Apply stopword removal
	sentences = text.lower()
	cleaned = remove_punctuations(sentences).split()
	tokens = [token for token in cleaned if token not in STOP_WORDS_SET]
	return tokens

def regex_tokenizer(text):
	"""
	Instead of a naive approach to tokenize words + removing stop words, I'll use `re` or regex for
	more precise tokenizing and avoid blindly deleting punctuations and select valid tokens only from
	the raw text.
	"""
	pattern = re.compile(
    		r"""
			[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+  # emails
			|\$(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?		# money like $1200 or $199.99
			|[0-9]+:[0-9]+					# time like 5:00
			|[A-Za-z0-9'’]+					# words in general
		""",
		re.VERBOSE,				
	)
	matches = pattern.finditer(text)
	cleaned = [m.group().lower() for m in matches]
	tokens = [token for token in cleaned if token not in STOP_WORDS_SET]
	return tokens




















