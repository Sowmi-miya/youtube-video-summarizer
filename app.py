import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Function to fetch transcript from YouTube
def get_transcript(youtube_url):
    video_id = youtube_url.split("v=")[-1] if "v=" in youtube_url else youtube_url.split("/")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([part['text'] for part in transcript])
    return full_transcript

# Function to summarize text
def summarize_text(text):
    max_chunk = 1000
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
    summary = ""
    for chunk in chunks:
        summary_part = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summary += summary_part[0]['summary_text'] + "\n"
    return summary

# Streamlit main function
def main():
    st.title("🎥 YouTube Video Summarizer (Hugging Face Version)")
    link = st.text_input("Enter the link of the YouTube video you want to summarize:")

    if st.button("Start"):
        if link:
            try:
                st.info("📄 Fetching transcript...")
                transcript = get_transcript(link)
                st.success("✅ Transcript loaded!")

                st.info("🧠 Summarizing...")
                summary = summarize_text(transcript)

                st.markdown("### 📝 Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a valid YouTube link.")

if __name__ == "__main__":
    main()     