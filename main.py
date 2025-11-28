"""
This file is my main and is responsible to importing all my functions and also handling
the parameters in the CLI.
"""

from stats import basic_counts, top_k_words, word_length, sentence_statistics
from rule_based import remove_stopwords, regex_tokenizer, regex_sentiment_analysis, regex_topic_assigner

def main():
	#text = """Apple (AAPL) shares fell 3.2% in pre-market trading after the company reported lower-than-expected iPhone sales for Q4. Revenue came in at $88.3B, missing analyst estimates of $90.1B, while EPS was $1.23, slightly above expectations. Management issued softer guidance for the upcoming quarter, citing weak demand in Europe and FX headwinds. Despite the sales shortfall, CEO Tim Cook emphasized “resilient services growth,” with services revenue rising 12% YoY. Analysts at Morgan Stanley said they remain “constructive” on the stock over the long term, but warned that short-term volatility is likely until macro conditions stabilize."""	

	text = """In Hong Kong, a city where millions of residents sleep, eat and work high above the ground in towers pressed together like books on a shelf, there has long been the threat that a massive fire could trap people inside their high-rises.

By Thursday, the scale of that nightmare emerged, as an inferno that had begun a day earlier with one 32-story building and quickly engulfed six other towers at an aging apartment complex became the deadliest fire in Hong Kong’s modern history. On Friday morning, the authorities said that at least 94 people had died in the blaze and dozens of others were still unaccounted for.

Hundreds of firefighters worked to put out flames that continued to burn in three buildings of the Wang Fuk Court complex in Tai Po district 24 hours after they were first reported on Wednesday afternoon. They searched for survivors who had been trapped inside the buildings, pulling both people and corpses out.

More than 70 others were in the hospital, some in critical condition. Outside a nearby community center, dozens of people whose relatives were missing waited in line within a police cordon to see if their loved ones were among those whose bodies had been found.

Investigators began piecing together how the flames had moved so swiftly, homing in on the green construction netting that had shrouded the buildings slated for renovation, as well as polystyrene foam that had apparently been installed on windows. The police arrested two directors and a consultant linked to a construction company that had installed the construction materials, saying they were suspected of manslaughter and gross negligence.

Image"""

	print("Original text ---> ", text)	

	print("")
	print("<<<<<<<<<<<<<<< BASIC CHARACTERS, WORDS, AND SENTENCES STATISTICS >>>>>>>>>>>>>>>")
	
	print("")

	num_chars, num_words, num_sent = basic_counts(text)
	print("Basic Counts --->")
	print("Number of characters: ", num_chars)
	print("Number of words: ", num_words)
	print("Number of sentences: ", num_sent)
	
	print("")

	print("Word Statistics --->")
	k = int(input("Enter your k value: "))
	k_words = top_k_words(text, k)
	print("Top K most frequent words: ", k_words)
	longest_word, shortest_word, average_word_len = word_length(text)
	print("Longest word: ", longest_word)
	print("Shortest word: ", shortest_word)
	print("Average word length: ", average_word_len)
		
	print("")

	print("Sentence Statistics --->")
	longest_sentence, shortest_sentence, average_sentence_count = sentence_statistics(text)
	print("Longest sentence: ", longest_sentence)
	print("Shortest sentence: ", shortest_sentence)
	print("Average word count for all sentences: ", average_sentence_count)
	
	print("")
	print("<<<<<<<<<<<<<<< STOP WORDS, REGEX, RULE-BASED  >>>>>>>>>>>>>>>")
	
	print("")
	
	tokens_no_stopwords = remove_stopwords(text)
	print("Naive tokens: ", tokens_no_stopwords)
	
	print("")
	
	regex_tokens = regex_tokenizer(text)
	print("Regex tokens: ", regex_tokens)
	
	print("")

	print("Updated basic counts after stop words removal (regex) --->")
	regex_text = " ".join(regex_tokens)
	num_chars, num_words, num_sent = basic_counts(regex_text)
	print("Number of content tokens(non-stopwords): ", num_words)
	
	print("Updated word statistics after stop words removal (regex) --->")
	k = int(input("Enter your k value: "))
	k_words = top_k_words(regex_text, k)
	print("Top-k content words: ", k_words)
	longest_word, shortest_word, average_word_len = word_length(regex_text)
	print("Average token length: ", average_word_len)
	
	print("")

	sentiment_score = regex_sentiment_analysis(regex_tokens)
	if sentiment_score > 0:
		print("This is an overall positive text with score of: ", sentiment_score)
	elif sentiment_score < 0:
		print("This is an overall negative text with score of: ", sentiment_score)
	elif sentiment_score == 0:
		print("This is a neutral text with the score of: ", sentiment_score)
	
	print("")
	
	topic = regex_topic_assigner(regex_tokens)
	print("The topic of this text is: ", topic)	

if __name__ == "__main__":
	main()
