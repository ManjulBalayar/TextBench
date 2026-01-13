import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title("Benchmark Results")
st.write("Comparative analysis of three NLP approaches for sentiment analysis on 12,000 restaurant reviews.")

st.divider()

# Dataset Overview
st.header("Dataset Overview")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Reviews", "12,000")
with col2:
    st.metric("Sentiment Classes", "3 (Positive, Neutral, Negative)")

st.write("""
**Data Distribution:** Reviews were balanced across sentiment classes based on ratings:
- Ratings 1-2 → Negative
- Rating 3 → Neutral  
- Ratings 4-5 → Positive
""")

st.write("""
**Test Set Sizes (different per approach):**
- Rule-Based: 12,000 samples (full dataset)
- BERT: 1,200 samples (10% held out for testing)
- LLM: 120 samples (due to API cost constraints)
""")

st.divider()

# Performance Comparison
st.header("Performance Comparison")

# Create performance dataframe
performance_data = pd.DataFrame({
    'Approach': ['Rule-Based', 'BERT', 'LLM (Gemini 2.5 Flash)'],
    'Test Set Size': ['12,000', '1,200', '120'],
    'Accuracy': [0.409, 0.71, 0.74],
    'Precision (Macro Avg)': [0.51, 0.71, 0.73],
    'Recall (Macro Avg)': [0.41, 0.71, 0.73],
    'F1-Score (Macro Avg)': [0.37, 0.71, 0.73]
})

st.dataframe(performance_data.style.highlight_max(axis=0, subset=['Accuracy', 'Precision (Macro Avg)', 'Recall (Macro Avg)', 'F1-Score (Macro Avg)']), use_container_width=True)

# Accuracy Comparison Chart
st.subheader("Accuracy Comparison")
fig = go.Figure(data=[
    go.Bar(
        x=performance_data['Approach'],
        y=performance_data['Accuracy'] * 100,
        text=[f"{val:.1f}%" for val in performance_data['Accuracy'] * 100],
        textposition='auto',
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
])
fig.update_layout(
    yaxis_title="Accuracy (%)",
    yaxis=dict(range=[0, 100]),
    height=400,
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Per-Class Performance
st.header("Per-Class Performance")

st.subheader("F1-Scores by Sentiment Class")
class_performance = pd.DataFrame({
    'Class': ['Negative', 'Neutral', 'Positive'] * 3,
    'Approach': ['Rule-Based']*3 + ['BERT']*3 + ['LLM']*3,
    'F1-Score': [
        0.56, 0.17, 0.48,  # Rule-based
        0.72, 0.63, 0.78,  # BERT
        0.75, 0.63, 0.81   # LLM
    ]
})

fig2 = px.bar(class_performance, x='Class', y='F1-Score', color='Approach',
              barmode='group',
              color_discrete_map={'Rule-Based': '#FF6B6B', 'BERT': '#4ECDC4', 'LLM': '#45B7D1'})
fig2.update_layout(height=400, yaxis=dict(range=[0, 1]))
st.plotly_chart(fig2, use_container_width=True)

st.write("""
**Key Observations:**
- All approaches struggle most with the **neutral** class
- LLM performs best on **positive** sentiment (F1: 0.81)
- BERT shows balanced performance across all classes
- Rule-based heavily favors **negative** predictions due to limited vocabulary
""")

st.divider()

# Speed & Resources Comparison
st.header("Speed & Resource Requirements")

resource_data = pd.DataFrame({
    'Approach': ['Rule-Based', 'BERT', 'LLM'],
    'Avg Latency': ['< 0.001s', '~0.05-0.2s', '~1-3s'],
    'Model Size': ['N/A (word lists)', '~440 MB', 'API-based'],
    'Training Required': ['No', 'Yes (fine-tuning)', 'No (prompt-based)'],
    'Cost': ['Free', 'One-time GPU cost', 'API calls ($)']
})

st.dataframe(resource_data, use_container_width=True)

st.divider()

# Trade-offs Summary
st.header("Trade-offs Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Rule-Based")
    st.write("**Pros:**")
    st.write("- Extremely fast")
    st.write("- No training needed")
    st.write("- Fully interpretable")
    st.write("- Zero cost")
    st.write("")
    st.write("**Cons:**")
    st.write("- Low accuracy (41%)")
    st.write("- Limited vocabulary")
    st.write("- No context understanding")
    st.write("- Manual maintenance")

with col2:
    st.subheader("BERT")
    st.write("**Pros:**")
    st.write("- Good accuracy (71%)")
    st.write("- Context-aware")
    st.write("- One-time training")
    st.write("- Fast inference")
    st.write("")
    st.write("**Cons:**")
    st.write("- Requires training data")
    st.write("- GPU needed for training")
    st.write("- Limited to 128 tokens")
    st.write("- Model storage required")

with col3:
    st.subheader("LLM")
    st.write("**Pros:**")
    st.write("- Best accuracy (74%)")
    st.write("- No training needed")
    st.write("- Provides reasoning")
    st.write("- Easy to adjust via prompts")
    st.write("")
    st.write("**Cons:**")
    st.write("- Slowest (1-3s)")
    st.write("- API costs")
    st.write("- Rate limits")
    st.write("- Less predictable")

st.divider()

# Recommendations
st.header("Recommendations")

st.write("""
**Choose based on your use case:**

- **Rule-Based**: Best for simple filtering, real-time processing of massive volumes, or when accuracy isn't critical
- **BERT**: Ideal for production systems needing good accuracy with predictable latency and no ongoing API costs
- **LLM**: Best when highest accuracy is needed, training data is limited, or you need explanations for predictions

**For most production use cases**, BERT offers the best balance of accuracy, speed, and cost-effectiveness after initial fine-tuning.
""")