import streamlit as st
import requests
from gtts import gTTS


from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the API key
API_KEY = os.getenv("API_KEY")



# Function to fetch Hindi news from NewsData API
def fetch_news(company_name):
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={company_name}&language=hi"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("results", [])
        return articles[:5]  # Return top 5 articles
    return []

# Function to generate text-to-speech audio in Hindi
def generate_audio(text, filename="headline.mp3"):
    tts = gTTS(text=text, lang="hi")  # Convert text to Hindi speech
    tts.save(filename)
    return filename

# Streamlit UI
def main():
    st.set_page_config(page_title="News And Audio", layout="wide")
    st.title("📰 News And Audio")

    company_name = st.text_input("Search the company name:", "Google")
    
    if st.button("Analyze"):
        with st.spinner(f"{company_name} के लिए समाचार प्राप्त कर रहे हैं..."):
            articles = fetch_news(company_name)
        
        if not articles:
            st.error("कोई प्रासंगिक समाचार नहीं मिला। कृपया किसी अन्य कंपनी को आज़माएं।")
        else:
            for i, article in enumerate(articles):
                title = article.get("title", "कोई शीर्षक उपलब्ध नहीं")
                link = article.get("link", "#")
                
                st.subheader(title)
                st.write(f"[पूरा लेख पढ़ें]({link})")
                
                # Generate and play audio in Hindi
                audio_file = generate_audio(title, f"headline_{i}.mp3")
                with open(audio_file, "rb") as audio:
                    st.audio(audio, format="audio/mp3")

if __name__ == "__main__":
    main()
