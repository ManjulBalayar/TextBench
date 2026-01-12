"""
This file is my main and is responsible to importing all my functions and also handling
the parameters in the CLI.
"""

from src.utils.stats import basic_counts, top_k_words, word_length, sentence_statistics
from src.rule_based import remove_stopwords, regex_tokenizer, regex_sentiment_analysis, regex_topic_assigner
from src.bert_based import bert_tokenizer, bert_predict

def main():
#    text = """I like that this has just simple ingredients for barrier repair and gentle preservatives. I do medical microneedling and was looking for something simple to use the following day that would help my skin heal. I normally just use shea butter and hyaluronic acid and zinc sunscreen. Unfortunately, this product did not work for the day after needling. It made my skin sting so I rinsed it off. But after a few days I started using this topped with a dab of shea butter and wow my skin has never been so hydrated and smooth. I normally have a dehydration line and flakimess, but both of those issues were almost gone after a couple weeks. With it being so cheap, it's worth a try if you have barrier/dehydration issues. I think the combo of ceramides and fatty acids and the lack of actives makes a difference. I am prone to clogged pores but this did not make them worse. Sometimes the old tried and true skincare formulations just work better.
#    """
    #text = """Not bad. Very light on the skin. It’s a decent sized bottle that can last a couple of months it feels hydrating for a while, but as the winter came I felt I needed to use it again after a few hours"""
    text = """I am so impressed with the Vanicream Daily Facial Moisturizer. My skin is very sensitive, and this is one of the only products that keeps it calm, hydrated, and irritation-free. It has a smooth, lightweight texture that absorbs quickly without leaving my face greasy or sticky.
I also love that it’s fragrance-free and packed with hyaluronic acid and ceramides — my skin feels soft, balanced, and moisturized all day long. After using it consistently, I can definitely see a difference in how healthy and even my skin looks.
If you have sensitive or acne-prone skin, I highly recommend this. I’m genuinely satisfied with my results and will absolutely repurchase! """
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

    print("")

    bert_tokens = bert_tokenizer(text)
    print("BERT Tokens: ", bert_tokens)
    
    print("")

    bert_sentiment = bert_predict(text)
    print("BERT Sentiment Analysis: ", bert_sentiment)

if __name__ == "__main__":
    main()
