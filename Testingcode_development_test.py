# import streamlit as st
# from youtube_transcript_api import YouTubeTranscriptApi
# import yt_dlp
# import whisper
# import google.generativeai as genai
# import re
# import os

# # Set your Gemini API key
# genai.configure(api_key=st.secrets["GENI_API_KEY"])

# st.title("🎥 YouTube Video Summarizer + Chatbot (Gemini 1.5 Flash)")

# video_url = st.text_input("YouTube Video URL")

# def get_video_id(url):
#     pattern = r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})"
#     match = re.search(pattern, url)
#     return match.group(1) if match else None

# def fetch_transcript(video_id):
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript_text = " ".join([t['text'] for t in transcript_list])
#         return transcript_text
#     except:
#         return None

# def download_audio(url, video_id):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'quiet': True,
#         'outtmpl': f'{video_id}.%(ext)s',   # unique filename for each video
#         'noplaylist': True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         audio_file = ydl.prepare_filename(info)
#     return audio_file

# def transcribe_audio(audio_file):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file)
#     return result["text"]

# def summarize_with_gemini(text):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     prompt = f"Summarize the following text concisely:\n\n{text}"
#     response = model.generate_content(prompt)
#     return response.text

# def chat_with_gemini(context, user_question):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     prompt = f"""
# You are a helpful assistant. Use the following video transcript/summary as context:

# {context}

# Now answer the user's question clearly and concisely.
# Question: {user_question}
# """
#     response = model.generate_content(prompt)
#     return response.text

# # --- MAIN LOGIC ---
# if st.button("Summarize Video"):
#     if not video_url:
#         st.error("Please enter a YouTube video URL.")
#     else:
#         video_id = get_video_id(video_url)
#         if not video_id:
#             st.error("Invalid YouTube URL.")
#         else:
#             message_placeholder = st.empty()

#             # Step 1: Fetch transcript
#             message_placeholder.info("Trying to fetch YouTube transcript...")
#             transcript_text = fetch_transcript(video_id)
#             if transcript_text:
#                 message_placeholder.success("Transcript fetched successfully!")
#             else:
#                 message_placeholder.warning("Transcript not available. Falling back to audio transcription...")

#                 # Step 2: Download + Transcribe
#                 try:
#                     message_placeholder.info("Downloading audio...")
#                     audio_file = download_audio(video_url, video_id)
#                     message_placeholder.success(f"Audio downloaded as {os.path.basename(audio_file)}")

#                     message_placeholder.info("Transcribing audio...")
#                     transcript_text = transcribe_audio(audio_file)
#                     message_placeholder.success("Audio transcribed successfully!")
#                 except Exception as e:
#                     message_placeholder.error(f"Failed to transcribe audio: {e}")
#                     transcript_text = None

#             # Step 3: Summarize
#             if transcript_text:
#                 try:
#                     message_placeholder.info("Generating summary with Gemini 1.5 Flash...")
#                     summary_text = summarize_with_gemini(transcript_text)
#                     message_placeholder.success("Summary generated successfully!")
#                     st.subheader("📌 Video Summary")
#                     st.write(summary_text)

#                     # Save transcript + summary in session state for chatbot
#                     st.session_state["context"] = transcript_text + "\n\nSummary:\n" + summary_text

#                 except Exception as e:
#                     message_placeholder.error(f"Failed to summarize transcript: {e}")

# # --- CHATBOT SECTION ---
# if "context" in st.session_state:
#     st.subheader("🤖 Ask Questions about the Video")
#     user_question = st.text_input("Type your question here:")
#     if st.button("Ask"):
#         if user_question.strip():
#             try:
#                 answer = chat_with_gemini(st.session_state["context"], user_question)
#                 st.markdown(f"**Answer:** {answer}")
#             except Exception as e:
#                 st.error(f"Chatbot error: {e}")
#         else:
#             st.warning("Please enter a question.")




import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import whisper
import google.generativeai as genai
import re
import os

# Set your Gemini API key
genai.configure(api_key=st.secrets["GENI_API_KEY"])

st.title("🎥 YouTube Summarizer + 🤖 Chatbots")

video_url = st.text_input("YouTube Video URL")

def get_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript_list])
        return transcript_text
    except:
        return None

def download_audio(url, video_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': f'{video_id}.%(ext)s',   # unique filename for each video
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info)
    return audio_file

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

def summarize_with_gemini(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the following text concisely:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

def chat_with_gemini(context, user_question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are a helpful assistant. Use the following context if provided:

{context if context else "No context provided."}

Now answer the user's question clearly and concisely.
Question: {user_question}
"""
    response = model.generate_content(prompt)
    return response.text

# --- VIDEO SUMMARIZER ---
if st.button("Summarize Video"):
    if not video_url:
        st.error("Please enter a YouTube video URL.")
    else:
        video_id = get_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL.")
        else:
            message_placeholder = st.empty()

            # Step 1: Fetch transcript
            message_placeholder.info("Trying to fetch YouTube transcript...")
            transcript_text = fetch_transcript(video_id)
            if transcript_text:
                message_placeholder.success("Transcript fetched successfully!")
            else:
                message_placeholder.warning("Transcript not available. Falling back to audio transcription...")

                # Step 2: Download + Transcribe
                try:
                    message_placeholder.info("Downloading audio...")
                    audio_file = download_audio(video_url, video_id)
                    message_placeholder.success(f"Audio downloaded as {os.path.basename(audio_file)}")

                    message_placeholder.info("Transcribing audio...")
                    transcript_text = transcribe_audio(audio_file)
                    message_placeholder.success("Audio transcribed successfully!")
                except Exception as e:
                    message_placeholder.error(f"Failed to transcribe audio: {e}")
                    transcript_text = None

            # Step 3: Summarize
            if transcript_text:
                try:
                    message_placeholder.info("Generating summary with Gemini 1.5 Flash...")
                    summary_text = summarize_with_gemini(transcript_text)
                    message_placeholder.success("Summary generated successfully!")
                    st.subheader("📌 Video Summary")
                    st.write(summary_text)

                    # Save transcript + summary in session state for chatbot
                    st.session_state["video_context"] = transcript_text + "\n\nSummary:\n" + summary_text

                except Exception as e:
                    message_placeholder.error(f"Failed to summarize transcript: {e}")

# --- VIDEO CHATBOT ---
if "video_context" in st.session_state:
    st.subheader("🤖 Ask Questions about the Video")
    user_question = st.text_input("Type your video-related question here:", key="video_q")
    if st.button("Ask Video Bot"):
        if user_question.strip():
            try:
                answer = chat_with_gemini(st.session_state["video_context"], user_question)
                st.markdown(f"**Video Bot Answer:** {answer}")
            except Exception as e:
                st.error(f"Video chatbot error: {e}")
        else:
            st.warning("Please enter a question.")

# --- GENERAL CHATBOT ---
st.subheader("💬 General Chatbot")
general_question = st.text_input("Ask me anything:", key="general_q")
if st.button("Ask General Bot"):
    if general_question.strip():
        try:
            answer = chat_with_gemini("", general_question)  # no context, free chat
            st.markdown(f"**General Bot Answer:** {answer}")
        except Exception as e:
            st.error(f"General chatbot error: {e}")
    else:
        st.warning("Please enter a question.")
