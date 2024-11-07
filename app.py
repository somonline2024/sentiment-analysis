# app.py
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Sample data for demonstration (replace with your actual DataFrame)
data = {
    'Sentiment': ['Positive', 'Neutral', 'Negative', 'Positive', 'Neutral', 'Negative', 'Positive'],
    'Confidence': [0.95, 0.6, 0.8, 0.92, 0.55, 0.7, 0.88]
}
df = pd.DataFrame(data)

# Set style for Seaborn plots
sns.set_style("whitegrid")

# Streamlit app
st.title("Sentiment Analysis Visualizations")

# 1. Count Plot with Annotations
st.subheader("Sentiment Distribution of Employee Feedback")
fig, ax = plt.subplots(figsize=(10, 6))
sentiment_plot = sns.countplot(data=df, x='Sentiment', palette='Set2', ax=ax)
plt.title('Sentiment Distribution of Employee Feedback', fontsize=16, weight='bold')
plt.xlabel('Sentiment', fontsize=14)
plt.ylabel('Number of Feedback Entries', fontsize=14)

# Add annotations on bars
for p in sentiment_plot.patches:
    sentiment_plot.annotate(f'{int(p.get_height())}',
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),
                            textcoords='offset points')
st.pyplot(fig)

# 2. Box Plot for Confidence Scores by Sentiment
st.subheader("Confidence Score Distribution by Sentiment")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x='Sentiment', y='Confidence', palette='Set3', ax=ax)
plt.title('Confidence Score Distribution by Sentiment', fontsize=16, weight='bold')
plt.xlabel('Sentiment', fontsize=14)
plt.ylabel('Confidence Score', fontsize=14)
st.pyplot(fig)

# 3. Box Plot with Swarm Plot Overlay for Confidence Scores by Sentiment
st.subheader("Confidence Scores by Sentiment (Detailed View)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x='Sentiment', y='Confidence', palette='Set3', showfliers=False, ax=ax)  # Box plot without outliers
sns.swarmplot(data=df, x='Sentiment', y='Confidence', color='k', alpha=0.6, ax=ax)             # Overlay swarm plot
plt.title('Confidence Scores by Sentiment (Detailed View)', fontsize=16, weight='bold')
plt.xlabel('Sentiment', fontsize=14)
plt.ylabel('Confidence Score', fontsize=14)
st.pyplot(fig)