# TextBench

What is this? Well, it's a fun little project that benchmarks and compares different NLP approaches for text analysis. I'm comparing rule-based techniques (regex tokenization), transformer models (BERT), and eventually LLMs to see how they stack up against each other for sentiment analysis, topic classification, and summarization. The goal is to understand the trade-offs between speed, accuracy, and complexity across these different methods, with visualizations to make it all clear. 

## `stats.py`

In this file I created basic statistics on the text such as:

- Basic counts (num of chars, num of words, num of sentences)
- Word statistics (Top k-most freq words, longest & shortest words, average word length)
- Sentence statistics (Average sentence in words, shortest & longest sentence)

I did this without any external libraries used and purely from scratch, far from perfect but about average considering I'm not using spacy or nltk, etc.

## `rule_based.py`

This file I focused more on rule-based techniques, primarily working with Python's `re` library. But first I implemented my own stopwords removal from scratch. I make a large lookup translate table with a pre-defined set of common stopwords. Not perfect again but this is average I guess for not using any special libraries or ML. Next I use the `re` libray to remove stopwords using regex now. And it performs better and is able to pick up things like emails, URLs, money like $199,999, and put it as one token. Pretty cool, and I actually like this since I can decide for myself what to keep and what not to keep. I then try to capture the sentiment on whether it is positive, negative, or neutral by detecting words in the given text file. And lastly, rule-based topics detection like 'tech', 'finance', 'politics', etc. All of this was also completely rule-based and made from scratch by me.

## `semantics.py`

This is where the BERT magic happens (still in progress). I'll be implementing transformer-based sentiment analysis, topic classification, and abstractive summarization using pre-trained BERT models. The plan is to compare these results directly against my rule-based approach to see where transformers shine and where simple regex is actually good enough. Spoiler: I'm expecting BERT to be more accurate but way slower, which is the whole point of this benchmark.

## The Benchmark

The endgame here is to create side-by-side comparisons with metrics like accuracy, F1-scores, and processing speed. Plus, I'll throw in some visualizations (word clouds, sentiment distributions, topic trends) to make the data actually interesting to look at. It's not just about building models—it's about understanding when to use which approach in the real world.

