import streamlit as st
import pandas as pd

# Load the dataset
file_path = "D:\\NewDataSet.csv"  # Make sure the file path is accessible in the environment
df = pd.read_csv(file_path)

# Ensure 'Genres' column is treated as a string
df['Genres'] = df['Genres'].astype(str).fillna('')

# Convert 'User Score' to numeric, handling non-numeric values
df['User Score'] = pd.to_numeric(df['User Score'], errors='coerce')

# Function to get user preferences via Streamlit inputs
def get_user_preferences():
    genres = st.text_input("Enter your preferred genre:").strip()
    min_user_score = st.number_input("Enter your minimum acceptable user score:", min_value=0.0)
    return {
        'Genres': genres,
        'Minimum User Score': min_user_score
    }

# Function to recommend games based on user preferences
def recommend_games(df, preferences):
    # Check for 'Genres' and 'User Score' columns
    if 'Genres' not in df.columns or 'User Score' not in df.columns:
        raise ValueError("The dataset must contain 'Genres' and 'User Score' columns.")
    
    # Filter by genre
    genre_filter = df['Genres'].str.contains(preferences['Genres'], case=False, na=False)
    
    # Filter by user score
    score_filter = df['User Score'] >= preferences['Minimum User Score']
    
    # Apply filters
    filtered_df = df[genre_filter & score_filter]
    
    return filtered_df

# Main Streamlit app logic
st.title("Game Recommendation System")

# Get User Preferences
user_preferences = get_user_preferences()

# Recommend Games
if user_preferences['Genres']:  # Check if genres input is provided
    try:
        recommended_games = recommend_games(df, user_preferences)
        
        if not recommended_games.empty:
            # Show top 10 recommendations
            top_10_games = recommended_games.head(10)
            st.write("Top 10 Recommended Games based on your preferences:")
            st.dataframe(top_10_games)
        else:
            st.write("No games match your preferences.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
