# TextAnalyzer

What is this? Well, it's a fun little project that gives you basic stats, patterns + sentiment analysis using regex, and semantic understandings of any text file that you give it. Ignore the `.swp` files, those are files generated from me using Vim. Yup, I'm cool like that. 

## `stats.py`

In this file I created basic statistics on the text such as:

- Basic counts (num of chars, num of words, num of sentences)
- Word statistics (Top k-most freq words, longest & shortest words, average word length)
- Sentence statistics (Average sentence in words, shortest & longest sentence)

I did this without any external libraries used and purely from scratch, far from perfect but about average considering I'm not using spacy or nltk, etc.

## `rule_based.py`

This file I focused more on rule-based techniques, primarily working with Python's `re` library. But first I implemented my own stopwords removal from scratch. I make a large lookup translate table with a pre-defined set of common stopwords. Not perfect again but this is average I guess for not using any special libraries or ML. Next I use the `re` libray to remove stopwords using regex now. And it performs better and is able to pick up things like emails, URLs, money like $199,999, and put it as one token. Pretty cool, and I actually like this since I can decide for myself what to keep and what not to keep. I then try to capture the sentiment on whether it is positive or negative by detecting words in the given text file. And lastly, rule-based topics detection like 'tech', 'finance', 'customer', etc.

