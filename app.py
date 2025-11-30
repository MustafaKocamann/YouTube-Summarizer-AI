import streamlit as st
import os
import re
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai

# youtube-transcript-api v1.2.x için doğru import
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# --- CONFIGURATION AND CONSTANTS ---
load_dotenv()

SYSTEM_PROMPT = """
### ROLE AND OBJECTIVE
You are a "Senior Content Analyst & Summarizer AI" specialized in processing complex video transcripts. Your task is to read the provided video transcript, understand the context, and distill the most valuable information for the user into a structured summary.

### CORE RULES (SAFETY & ETHICS)
1. ZERO HALLUCINATION POLICY: Base your output STRICTLY on the provided text.
2. OBJECTIVITY: Reflect the speaker's ideas exactly as they are.
3. STRUCTURE: Follow the Markdown format strictly.

### OUTPUT FORMAT
# [Video Main Title/Topic]

## 🎯 TL;DR (One-Sentence Summary)
(Summarize what the video is about in max 2 sentences)

## 🔑 Key Takeaways
(List the 3-5 most important points as bullet points)

## 📝 Detailed Summary
(Explain the video content in logical paragraphs using fluent language.)

## 💡 Conclusion & Action Items
(Any final conclusion or advice)
"""

# --- HELPER CLASSES ---


class YouTubeService:
    """Handles YouTube-related operations (ID extraction, Transcript retrieval)."""

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extracts Video ID from various YouTube URL formats.
        """
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def get_transcript(video_id: str) -> Optional[str]:
        """
        Fetches the transcript based on Video ID using youtube-transcript-api>=1.2.0.
        """
        try:
            # Yeni API: instance oluşturup fetch kullanıyoruz
            ytt_api = YouTubeTranscriptApi()

            # Önce Türkçe, sonra İngilizce dene (istersen dilleri değiştirebilirsin)
            fetched = ytt_api.fetch(video_id, languages=["tr", "en"])

            # FetchedTranscript -> raw dict list
            raw_data = fetched.to_raw_data()
            full_text = " ".join(item["text"] for item in raw_data)
            return full_text

        except TranscriptsDisabled:
            st.error(
                "Transcript Error: Subtitles are disabled for this video. (Altyazılar kapalı)"
            )
            return None
        except Exception as e:
            st.error(f"Transcript Error: {e}")
            return None


class GeminiProcessor:
    """Manages Google Gemini AI model interactions."""

    def _init_(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("API Key not found! Please check your .env file.")
            self.model = None
            return

        genai.configure(api_key=api_key)

        # Model adı; sen zaten 2.5 Flash kullanıyordun
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )

    def generate_summary(self, transcript_text: str) -> Optional[str]:
        """Sends the transcript to the model and retrieves the summary."""
        if not self.model:
            return None

        try:
            user_message = (
                "Here is the transcript:\n<transcript>\n"
                + transcript_text
                + "\n</transcript>"
            )
            response = self.model.generate_content(user_message)
            return response.text
        except Exception as e:
            st.error(f"AI Model Error: {e}")
            return None


# --- UI LAYER (STREAMLIT) ---


def main():
    st.set_page_config(page_title="YouTube Summarizer AI", page_icon="📺")
    st.title("📺 YouTube Video Summarizer")
    st.markdown("Professional video summarizer powered by *Gemini 2.5 Flash*.")

    youtube_service = YouTubeService()
    gemini_processor = GeminiProcessor()

    youtube_link = st.text_input("Paste YouTube Video Link:")

    if youtube_link:
        video_id = youtube_service.extract_video_id(youtube_link)

        if video_id:
            st.image(
                f"https://img.youtube.com/vi/{video_id}/0.jpg",
                caption="Video Thumbnail",
                use_container_width=True,
            )

            if st.button("Generate Summary 🚀"):
                with st.spinner("Fetching transcript and analyzing..."):
                    transcript_text = youtube_service.get_transcript(video_id)

                    if transcript_text:
                        summary = gemini_processor.generate_summary(transcript_text)

                        if summary:
                            st.success("Process Completed!")
                            st.markdown("---")
                            st.markdown(summary)
        else:
            st.warning("Please enter a valid YouTube link.")


if __name__ == "__main__":
    main()