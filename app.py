from pytube import YouTube
from flask import Flask, session, url_for, send_file, render_template, redirect, request
from io import BytesIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"

@app.route("/video/<video_id>", methods=["GET"])
def video(video_id):
    youtube_link = f"https://www.youtube.com/watch?v={video_id}"
    buffer = BytesIO()
    url = YouTube(youtube_link)
    
    # Select the stream with 1080p resolution (if available)
    video_stream = url.streams.filter(res="1080p", file_extension="mp4").first()

    if video_stream:
        video_stream.stream_to_buffer(buffer)
        buffer.seek(0)

        video_path = f"{url.title}.mp4"

        # Fetch and set the thumbnail image
        thumbnail_url = url.thumbnail_url
        thumbnail_data = BytesIO(YouTube(thumbnail_url).thumbnail_url)
        
        with open(video_path, "wb") as video_file:
            video_file.write(buffer.read())

        return send_file(video_path, as_attachment=True)

    return "Invalid or missing YouTube link parameter."

if __name__ == '__main__':
    app.run(debug=True)
