from pytube import YouTube
from flask import Flask, session, url_for, send_file, render_template, redirect, request
from io import BytesIO

app = Flask(__name)
app.config["SECRET_KEY"] = "my_secret_key"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        session["link"] = request.form.get("url")
        url = YouTube(session["link"])
        url.check_availability()
        return render_template("download.html", url=url)

    return render_template('index.html')

@app.route("/download", methods=["GET"])
def download():
    youtube_url = request.args.get("url")
    if youtube_url:
        buffer = BytesIO()
        url = YouTube(youtube_url)
        video = url.streams.get_highest_resolution()

        # Stream the video to the buffer
        video.stream_to_buffer(buffer)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name=video.title, mimetype=video.mime_type)
    else:
        return "Missing 'url' parameter in the query string."

if __name__ == '__main__':
    app.run(debug=True)

