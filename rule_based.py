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

POSITIVE = {
	"good", "great", "excellent", "amazing", "awesome", "positive", "fortunate",
    	"smooth", "successful", "well", "improved", "love", "nice", "happy",
    	"beneficial", "effective", "efficient", "fast", "quick", "stable",
    	"resolved", "fix", "fixed", "handle", "handled", "progress",
    	"supportive", "reliable", "success", "clean"	
}
POSITIVE_WORDS = set(POSITIVE)

NEGATIVE = {
	"bad", "terrible", "awful", "negative", "unfortunate",
    	"slow", "sluggish", "fail", "failed", "failure", "error", "errors",
    	"issue", "issues", "problem", "problems", "bug", "bugs",
    	"timeout", "crash", "broken", "downtime", "unstable",
    	"delay", "delayed", "incorrect", "poor", "worse", "worst",
    	"unexpected", "critical", "urgent",
    	"outdated", "dependency", "incident"
}
NEGATIVE_WORDS = set(NEGATIVE)

NEGATION = {"not", "no", "never", "none", "didn't", "won't", "cannot", "can't"}
NEGATION_WORDS = set(NEGATION)

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
	pattern = re.compile(
    		r"""
        	https?://\S+                                      # URLs
        	|[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+   # emails
        	|\$(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?[KMBkmb]?  # money: $88.3B, $1.23, $90M
        	|\d+(?:\.\d+)?%                                   # percentages: 3.2%, 12%
        	|[0-9]{1,2}:[0-9]{2}                              # times: 3:00, 12:30
        	|[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*                # words w/ internal - or '
    		""",
		re.VERBOSE,
	)
	matches = pattern.finditer(text)
	cleaned = [m.group().lower() for m in matches]
	tokens = [token for token in cleaned if token not in STOP_WORDS_SET]
	return tokens


def regex_sentiment_analysis(text):
	"""
	This function is responsible for understanding the sentiment of the text, ruling it out if it's a positive or a negative sentiment.
	We will keep a count for positive and negative words. Then in the end we will do a simple subtraction to calculate the sentiment score
	for the text. We also have negation words to handle things like "not good" ---> this should count as negative and not positive even though
	the text consists of the word "good". Meaning we always need to keep a window to 2 to make sure that we also consider what comes before
	these words.
	"""
	pos = 0
	neg = 0
	for i, w in enumerate(text):
		if i > 0 and i < len(text)-1:
			if w in POSITIVE_WORDS and text[i-1] not in NEGATION_WORDS:
				pos += 1
			elif w in POSITIVE_WORDS and text[i-1] in NEGATION_WORDS:
				neg += 1
			elif w in NEGATIVE_WORDS and text[i-1] in NEGATION_WORDS:
				pos += 1
			elif w in NEGATIVE_WORDS and text[i-1] not in NEGATION_WORDS:
				neg += 1
	sentiment_score = pos - neg
	return sentiment_score
