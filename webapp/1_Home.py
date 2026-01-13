import sys
import os
import time
import streamlit as st
from transformers import AutoTokenizer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.rule_based import regex_sentiment_analysis, regex_tokenizer
from src.bert_based import bert_tokenizer, bert_predict
from src.llm_based import llm_tokenizer, llm_sentiment_analysis

st.set_page_config(
    page_title="TextBench"
)

st.title("TextBench Demo")
st.write("This app benchmarks three different NLP approaches for sentiment analysis such as rule-based (regex), encoder-only model (BERT), and encoder-decoder model (gemini-flash-2.5). The goal is to see how they perform against each other and to understand the trade-offs between speed, accuracy, and complexity.")

st.write("You can write some text below and click the 'Analyze' button to see the results of the three approaches. Some examples of text you can try are:")
st.write("- 'Good food but prices could be cheaper. Overall, would recommend!'")
st.write("- 'Not bad. Very light on the skin. It’s a decent sized bottle that can last a couple of months it feels hydrating for a while, but as the winter came I felt I needed to use it again after a few hours'")
st.write("- 'I also love that it’s fragrance-free and packed with hyaluronic acid and ceramides — my skin feels soft, balanced, and moisturized all day long. After using it consistently, I can definitely see a difference in how healthy and even my skin looks.'")

st.write("You could if you want write a random sentence as well to see the results of the three approaches.")

st.sidebar.success("Select a page above.")

st.divider()
st.subheader("Demo your review (for a product, service, etc.) here:")
user_input = st.text_area("Enter your review", label_visibility="collapsed")

if st.button("Analyze"):
    if user_input:
        st.divider()
        
        # LLM-Based Analysis
        st.subheader("1. LLM-Based Analysis")
        start_time = time.time()
        llm_tokens = llm_tokenizer(user_input)
        
        # Check if tokenizer returned an error
        if isinstance(llm_tokens, dict) and 'error' in llm_tokens:
            st.error(f"**Tokenization Error:** {llm_tokens['error']}")
            llm_tokens = ["N/A"]
        
        st.write("**Tokens:**", llm_tokens)
        
        llm_result = llm_sentiment_analysis(user_input)
        llm_latency = time.time() - start_time
        
        # Check if sentiment analysis encountered an error
        if llm_result.get('sentiment') == 'error':
            st.error(f"**Analysis Error:** {llm_result['reasoning']}")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sentiment", llm_result['sentiment'].upper())
            with col2:
                st.metric("Confidence", f"{llm_result['confidence']}")
            with col3:
                st.metric("Latency", f"{llm_latency:.3f}s")
            if 'reasoning' in llm_result:
                st.write("**Reasoning:**", llm_result['reasoning'])
        
        st.divider()
        
        # BERT-Based Analysis
        st.subheader("2. BERT-Based Analysis")
        start_time = time.time()
        
        try:
            bert_tokens = bert_tokenizer(user_input)
            st.write("**Tokens:**", bert_tokens)
            
            # Check for truncation
            tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
            full_tokens = tokenizer.tokenize(user_input)
            if len(full_tokens) > 126:  # 128 - 2 special tokens ([CLS] and [SEP])
                st.warning(f"Text was truncated from {len(full_tokens)} to 126 tokens (BERT max_length=128 including special tokens)")
            
            bert_result = bert_predict(user_input)
            bert_latency = time.time() - start_time
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Prediction", bert_result['prediction'].upper())
            with col2:
                st.metric("Confidence", f"{bert_result['confidence']}%")
            with col3:
                st.metric("Latency", f"{bert_latency:.3f}s")
            
            st.write("**All Scores:**")
            for sentiment, score in bert_result['all_scores'].items():
                st.write(f"- {sentiment.capitalize()}: {score}%")
        except Exception as e:
            st.error(f"**BERT Analysis Error:** {str(e)}")
        
        st.divider()
        
        # Rule-Based Analysis
        st.subheader("3. Rule-Based Analysis")
        start_time = time.time()
        
        try:
            regex_tokens = regex_tokenizer(user_input)
            st.write("**Tokens:**", regex_tokens)
            
            regex_result = regex_sentiment_analysis(regex_tokens)
            regex_latency = time.time() - start_time
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Prediction", regex_result['prediction'].upper())
            with col2:
                st.metric("Positive Words", regex_result['num_of_pos_words'])
            with col3:
                st.metric("Negative Words", regex_result['num_of_neg_words'])
            with col4:
                st.metric("Latency", f"{regex_latency:.3f}s")
            st.write(f"**Confidence Score:** {regex_result['confidence']}")
        except Exception as e:
            st.error(f"**Rule-Based Analysis Error:** {str(e)}")
        
    else:
        st.warning("Please enter some text!")
