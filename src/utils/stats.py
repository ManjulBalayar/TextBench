"""
This file is responsible for generating the stats for my text input. Such as:
- Basic counts (num of chars, num of words, num of sentences)
- Word statistics (Top k-most freq words, longest & shortest words, average word length)
- Sentence statistics (Average sentence in words, shortest & longest sentence)
"""

PUNCT_TABLE = str.maketrans({".": "", "!":  "", "?": ""})

def basic_counts(text):
	# I love python. It's amazing!
	words = text.split()
	num_of_char = 0
	num_of_words = 0
	for word in words:
		num_of_words += 1
		for char in word:
			num_of_char += 1

	# Sentences are split up by periods, exclamation marks, question marks.
	end_list = {".", "?", "!"}
	end_set = set(end_list)
	
	sentence_count = 0
	if text[-1] in end_set:
		sentence_count = 1
	
	for i, c in enumerate(text):
		if c in end_set:
			if i > 0 and i < len(text)-1:
				if text[i-1] not in end_set and text[i+1] not in end_set:
					sentence_count += 1
				elif text[i-1] == "." and text[i+1] not in end_set and text[i+2] not in end_set:
					continue
				elif text[i-1] in end_set and text[i+1] not in end_set:
					sentence_count += 1

	return num_of_char, num_of_words, sentence_count

def top_k_words(text, k: int):
	# this could actually be used to generate some visualizations. 
	# some refreshers with matplotlib and maybe seaborn
	
	words = text.split()
	count = {}
	for i, word in enumerate(words):
		new_word = remove_punctuation(word)
		if new_word in count:
			count[new_word] += 1
		else:
			count[new_word] = 1
	return sorted(count, key=count.get, reverse=True)[:k]

def remove_punctuation(word):
	# Use translate() to replace multiple characters, replace() only replaces one character
	return word.translate(PUNCT_TABLE)

def word_length(text):
	words = text.split()
	cleaned = []

	for word in words:
		w = remove_punctuation(word)
		if w:
			cleaned.append(w)
	# Here, `cleaned` is a normal list, but I'm able to get it's length by setting the `key=len`
	longest_word = max(cleaned, key=len)
	shortest_word = min(cleaned, key=len)
	
	# sum of cleaned using list comprehension
	sums = sum(len(w) for w in cleaned)

	average_word_len = sums / len(cleaned)
	
	return longest_word, shortest_word, round(average_word_len)

# Sentence statistics, average sentence length in words. 
# Shortest and longest sentences by word count

def split_sentences(text):
        end_list = {".", "!", "?"}
        end_set = set(end_list)

        sentences = []
        s = ""
        for i, c in enumerate(text):
                if c not in end_set:
                        s += c
                else:
                        if i > 0 and i < len(text)-1:
                                if text[i-1] not in end_set and text[i+1] not in end_set:
                                        s += "|"
                                elif text[i-1] == "." and text[i+1] not in end_set and text[i+2] not in end_set:
                                        continue
                                elif text[i-1] in end_set and text[i+1] not in end_set:
                                        s += "|"
        sentences.append(s)

        my_string = sentences[0]
        final_sen = my_string.split("|")
        final_sen = [s.strip() for s in final_sen]
        return final_sen

def sentence_statistics(text):
        sentences = split_sentences(text)
        hashmap = {}
        for sen in sentences:
                hashmap[sen] = len(sen.split())

        longest_sentence = max(hashmap, key=hashmap.get)
        shortest_sentence = min(hashmap, key=hashmap.get)

        values = hashmap.values()
        total_sum = sum(values)
        count = len(values)
        average_sentence_count = total_sum / count
        return longest_sentence, shortest_sentence, round(average_sentence_count)
