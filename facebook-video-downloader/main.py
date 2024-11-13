from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class VideoURL(BaseModel):
    url: str

def download_facebook_video(url: str):
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',  # Use the video ID for the file name
        'format': 'best',  # Download the best available format
        'noplaylist': True,  # Ensure it's downloading only the video, not a playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Extract video info without downloading
            video_title = info_dict.get('title', None)
            video_url = info_dict.get('url', None)

            if video_url:
                # Download the video
                ydl.download([url])
                return {"status": "success", "title": video_title, "message": "Video downloaded successfully."}
            else:
                return {"status": "error", "message": "No valid video URL found."}
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {e}")
    except yt_dlp.utils.ExtractorError as e:
        raise HTTPException(status_code=500, detail=f"Extractor error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/download")
async def download_video(video: VideoURL):
    result = download_facebook_video(video.url)
    return result


@app.get("/")
async def root():
    return {"message": "Hello, World!"}