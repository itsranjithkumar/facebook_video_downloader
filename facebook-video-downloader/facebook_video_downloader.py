import yt_dlp

def download_facebook_video(url):
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
                print(f"Video found: {video_title}")
                print(f"Video URL: {video_url}")
                ydl.download([url])  # Start downloading the video
            else:
                print("No valid video URL found.")
    except yt_dlp.utils.DownloadError as e:
        print(f"Download failed: {e}")
    except yt_dlp.utils.ExtractorError as e:
        print(f"Extractor error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the Facebook video URL: ")
    download_facebook_video(video_url)



