from pytube import YouTube
from flask import Flask, session, send_file, request

app = Flask(__name)
app.config["SECRET_KEY"] = "my_secret_key"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        session["link"] = request.form.get("url")
        url = YouTube(session["link"])
        url.check_availability()
        return "Video URL submitted. <a href='/download'>Click here to download audio</a>"

    return "Enter a YouTube URL."

@app.route("/download", methods=["GET"])
def download():
    youtube_link = session.get("link")
    if youtube_link:
        url = YouTube(youtube_link)
        audio_stream = url.streams.filter(only_audio=True).first()

        if audio_stream:
            audio_stream.download(output_path="downloads/")
            return send_file(
                "downloads/" + audio_stream.default_filename,
                as_attachment=True,
                download_name=audio_stream.default_filename,
                mimetype="audio/mpeg"
            )

    return "Invalid or missing YouTube link parameter."

if __name__ == '__main__':
    app.run(debug=True)
