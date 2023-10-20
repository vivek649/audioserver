from pytube import YouTube
from flask import Flask, session, url_for, send_file, render_template, redirect, request
from io import BytesIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"

@app.route("/audio/<video_id>", methods=["GET"])
def audio(video_id):
    youtube_link = f"https://www.youtube.com/watch?v={video_id}"
    buffer = BytesIO()
    url = YouTube(youtube_link)
    audio_stream = url.streams.filter(only_audio=True).first()

    if audio_stream:
        audio_stream.stream_to_buffer(buffer)
        buffer.seek(0)

        # Set the ID3 tags for the audio file
        audio_file = buffer.read()
        audio_path = f"{url.title}.mp3"
        
        audio = eyed3.load(audio_path)
        audio.tag.artist = "Your Artist Name"
        audio.tag.title = url.title  # Use the video title as the audio title
        audio.tag.album = "Your Album"

        # Fetch and set the thumbnail image
        thumbnail_url = url.thumbnail_url
        thumbnail_data = BytesIO(YouTube(thumbnail_url).thumbnail_url)
        audio.tag.images.set(3, thumbnail_data.read(), "image/jpeg", "Thumbnail")

        audio.tag.save()

        return send_file(audio_path)

    return "Invalid or missing YouTube link parameter."

if __name__ == '__main__':
    app.run(debug=True)
