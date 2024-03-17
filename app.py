import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi as ytapi
import os
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
summary_model = genai.GenerativeModel("gemini-pro")
smprompt = """
Given to you will be the transcript of a video. Your job is to summarize the content in well structured, detailed, bullet points. Your main concern is to save the user's time by providing them the perfect summary of that video's transcription. Extract key important moments from the transcription, do not miss out on any useful information. Summarize everything in a bulleted format, almost as if you're generating notes. Most importantly, your summary should be a third person perspective, where the object is the video. Your summary must encapsulate everything that's happening in the video, from the start, in the middle, and till the end.

START OF EXAMPLE

"The video starts off with... <bullet points as title, add sub-points for details>.... and so on"

Your summary should give the users the sense as if they are watching the video themselves.

END OF EXAMPLE

Here's the transcription :
"""

def vid2txt(yt_link):
    video_id = yt_link.split("=")[1]
    transcript = ytapi.get_transcript(video_id)
    text_format = ""
    for i in range(len(transcript)):
        chunk = transcript[i]["text"]
        chunk = chunk.replace("\n", " ")
        text_format += " " + chunk
    return text_format

def summarize(url):
    ts = vid2txt(url)
    summary = summary_model.generate_content(f"{smprompt}\n{ts}").text
    return summary


@app.get("/")
async def derail():
    show = "You're not supposed to be here. Use the /get-summary/ endpoint."
    print(show)
    return show

@app.get("/get-summary/")
async def get_summary_from_url(text: str):
    result = summarize(text)
    return {"result":result}