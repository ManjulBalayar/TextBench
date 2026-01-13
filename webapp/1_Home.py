import streamlit as st

"""
Things I need to do in this page:
- Take user's raw text input
- Use that input to call tokenizer methods from each script(rule_based.py, bert_based.py, llm_based.py)
- Use sentiment analysis
"""

st.set_page_config(
    page_title="TextBench"
)

st.title("NLP Techniques Benchmarker For Sentiment Analysis Demo")
st.sidebar.success("Select a page above.")
