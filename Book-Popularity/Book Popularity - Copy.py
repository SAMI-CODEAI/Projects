import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Step 1: Load the dataset
data = pd.read_csv("books_data.csv")

# Step 2: Sentiment Analysis Function
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    return polarity

# Add Sentiment Scores
data['Sentiment'] = data['Post'].apply(get_sentiment)

# Step 3: Calculate Popularity Score
data['Popularity Score'] = (data['Likes'] + data['Comments']) * (1 + data['Sentiment'])

# Step 4: Aggregate Popularity by Book
aggregated_data = data.groupby('Book', as_index=False).agg({
    'Likes': 'sum',
    'Comments': 'sum',
    'Sentiment': 'mean',
    'Popularity Score': 'sum'
})

# Step 5: Identify Trending Books
top_books = aggregated_data.sort_values('Popularity Score', ascending=False).head(3)

# Step 6: Visualization Functions
def plot_popularity(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Book'], data['Popularity Score'], color='skyblue')
    plt.xlabel('Books')
    plt.ylabel('Popularity Score')
    plt.title('Book Popularity Based on Social Media Data')
    plt.show()

def plot_sentiment(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Book'], data['Sentiment'], color='lightcoral')
    plt.xlabel('Books')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment of Books')
    plt.show()

# Display Results
print("Aggregated Data:")
print(aggregated_data)
print("\nTop Trending Books:")
print(top_books)

# Step 7: Visualize Data
plot_popularity(aggregated_data)
plot_sentiment(aggregated_data)
