"""
This file is my main and is responsible to importing all my functions and also handling
the parameters in the CLI.
"""

from stats import basic_counts, top_k_words, word_length, sentence_statistics
from rule_based import remove_stopwords, regex_tokenizer

def main():
	text = """On October 12, 2024, our team deployed the new API service for client billing. The rollout was mostly smooth, but a few users reported “timeout” errors when processing invoices. According to our logs, the average response time increased from 230ms to nearly 480ms between 3:00 PM and 5:00 PM.

One engineer suggested that the issue might be related to an outdated dependency in the payment module. However, the fix requires coordination with the security team, and they won’t be available until next week.

We also received an urgent customer email at support@fintrack.io
 requesting a refund for a duplicate charge of $199.99. The customer shared a link to the failed invoice: https://fintrack.io/invoices/882133
. We should probably escalate this case to Level-2 support.

Overall, the team handled the situation well, but the incident highlights the need for better monitoring and automated alerts before major system changes."""	

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
		

if __name__ == "__main__":
	main()
