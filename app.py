 # app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from transformers import pipeline

# Initialize sentiment analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis")

# Function to analyze sentiment
def analyze_sentiment(feedback):
    result = sentiment_analysis(feedback)[0]
    return result['label'], result['score']

# Streamlit application
st.title("Employee Feedback Sentiment Analysis")

# File upload button
uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")

if uploaded_file is not None:
    # Read Excel file
    df = pd.read_excel(uploaded_file)

    # Perform sentiment analysis
    df['Sentiment'], df['Confidence'] = zip(*df['Feedback'].apply(analyze_sentiment))

    # Display the results
    st.write(df[['Name', 'Feedback', 'Sentiment', 'Confidence']])

    # Calculate the percentage of each sentiment type
    sentiment_counts = df['Sentiment'].value_counts(normalize=True) * 100

    # Determine overall sentiment
    if sentiment_counts.get('POSITIVE', 0) > 70:
        overall_sentiment = "Overall Sentiment: Positive"
    elif sentiment_counts.get('NEGATIVE', 0) > 70:
        overall_sentiment = "Overall Sentiment: Negative"
    else:
        overall_sentiment = "Overall Sentiment: Mixed Sentiment"

    # Display overall sentiment
    st.subheader(overall_sentiment)
    st.write(f"Positive Sentiment: {sentiment_counts.get('POSITIVE', 0):.2f}%")
    st.write(f"Negative Sentiment: {sentiment_counts.get('NEGATIVE', 0):.2f}%")
    st.write(f"Neutral Sentiment: {sentiment_counts.get('NEUTRAL', 0):.2f}%")

    # Visualization
    sns.set_style("whitegrid")

    # 1. Count Plot
    st.subheader("Sentiment Distribution")
    plt.figure(figsize=(10, 6))
    sentiment_plot = sns.countplot(data=df, x='Sentiment', palette='Set2')
    plt.title('Sentiment Distribution of Employee Feedback')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Feedback Entries')
    for p in sentiment_plot.patches:
        sentiment_plot.annotate(f'{int(p.get_height())}',
                                (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),
                                textcoords='offset points')
    st.pyplot(plt)

    # 2. Box Plot for Confidence Scores by Sentiment
    st.subheader("Confidence Score Distribution by Sentiment")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Sentiment', y='Confidence', palette='Set3')
    plt.title('Confidence Score Distribution by Sentiment')
    plt.xlabel('Sentiment')
    plt.ylabel('Confidence Score')
    st.pyplot(plt)

    # 3. Pie Chart to show sentiment distribution
    st.subheader("Team Sentiment Distribution")
    plt.figure(figsize=(8, 6))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#66c2a5', '#fc8d62', '#8da0cb'])
    plt.title(f"Team Sentiment Distribution - Overall Sentiment: {overall_sentiment}")
    st.pyplot(plt)

    # 4. Bar Chart to show sentiment distribution
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=['#66c2a5', '#fc8d62', '#8da0cb'])
    plt.title(f"Team Sentiment Distribution - Overall Sentiment: {overall_sentiment}")
    plt.xlabel("Sentiment Type")
    plt.ylabel("Percentage (%)")
    plt.ylim(0, 100)
    for index, value in enumerate(sentiment_counts.values):
        plt.text(index, value + 1, f"{value:.1f}%", ha='center')
    st.pyplot(plt)
