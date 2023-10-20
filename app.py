from pytube import YouTube
from flask import Flask, request, send_file
from io import BytesIO

# Create the Flask app and name it 'app'
app = Flask(__name)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_link = request.form.get("url")
        return redirect(f"/audio/{youtube_link}")
    return '''
    <form method="post">
        <input type="text" name="url" placeholder="Enter YouTube URL">
        <input type="submit" value="Download Audio">
    </form>
    '''

@app.route("/audio/<video_id>", methods=["GET"])
def audio(video_id):
    youtube_link = f"https://www.youtube.com/watch?v={video_id}"
    buffer = BytesIO()
    url = YouTube(youtube_link)
    audio_stream = url.streams.filter(only_audio=True).first()

    if audio_stream:
        audio_stream.stream_to_buffer(buffer)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name=f"{url.title}.mp3", mimetype="audio/mpeg")

    return "Invalid or missing YouTube link parameter."

if __name__ == '__main__':
    app.run(debug=True)


