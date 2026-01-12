# TextBench (NLP-Techniques Benchmarker For Sentiment Analysis)

TextBench benchmarks three different NLP approaches for sentiment analysis such as rule-based (regex), encoder-only model (BERT), and encoder-decoder model (gemini-flash-2.5). The goal is to see how they perform against each other and to understand the trade-offs between speed, accuracy, and complexity. I'm using a reviews dataset that contain ratings from 1-5, and our goal is to see if these techniques are able to pickup the sentiment of the reviews and rule out whether the review is `postive`, `neutral`, or `negative`.

## `rule_based.py`

This file I focused more on rule-based techniques, primarily working with Python's `re` library. But first I implemented my own stopwords removal from scratch. I make a large lookup translate table with a pre-defined set of common stopwords. Not perfect again but this is average I guess for not using any special libraries or ML. Next I use the `re` libray to remove stopwords using regex now. And it performs better and is able to pick up things like emails, URLs, money like $199,999, and put it as one token. Pretty cool, and I actually like this since I can decide for myself what to keep and what not to keep. I then try to capture the sentiment on whether it is positive, negative, or neutral by detecting words in the given text file. And lastly, rule-based topics detection like 'tech', 'finance', 'politics', etc. All of this was also completely rule-based and made from scratch by me.

## `BERT_Reviews.ipynb` & `bert_based.py`

The `notebooks/BERT_Reviews.ipynb` is where I perform the data preprocessing, create the PyTorch dataset & load it into the BERT model, and lastly train & test the sentiment classifer model using the pooled outputs from BERT. The model achieved an accuracy score of ~71% & the prediction time took around 4.5 minutes. But training had early stoppage around 5 epochs since BERT (that has a lot of params) can usually learn most relevant things by 2-5 epochs. By applying early stoppage once my macro-F1 plateaus, I can avoid overfitting. `src/bert_based.py` is just me loading the trained model to test raw text of our own.

## `LLM_Rule_Based_Reviews.ipynb` & `llm_based.py`

In this notebook, I tested both the LLM & rule-based techniques on my dataset. For the LLM, I tried zero-shot + a calibrated prompt achieving 71% & 74% accuracy on the same dataset (120 out 12000). Like the BERT model, the LLM model also struggled with `neutral` classes. Not to mention, LLM took a lot longer for only 120 data samples, the whole dataset is 12k. More analysis on the results are on the notebooks. The rule-based technique achieved a score of 40% on the whole dataset, but was pretty quick & not bad considering how short the sets were for positive, negative, and negation were. Although the rule-based predicted `neutral` for most cases since my logic was quite simple. 

## `stats.py`

In this file I created basic statistics on the text such as:

- Basic counts (num of chars, num of words, num of sentences)
- Word statistics (Top k-most freq words, longest & shortest words, average word length)
- Sentence statistics (Average sentence in words, shortest & longest sentence)

I did this without any external libraries used and purely from scratch, far from perfect but not bad considering I'm not using spacy or nltk, etc. I did this because the original project idea was a bit different, but it was fun to do it nonetheless so I decided to keep it.

## The Benchmark

The endgame here is to create side-by-side comparisons with metrics like accuracy, F1-scores, and processing speed.

