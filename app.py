from pytube import YouTube
from flask import Flask, session, send_file, request

app = Flask(__name)
app.config["SECRET_KEY"] = "my_secret_key"

@app.route("/download", methods=["GET"])
def download():
    youtube_link = request.args.get("url")
    if youtube_link:
        buffer = BytesIO()
        url = YouTube(youtube_link)
        audio_stream = url.streams.filter(only_audio=True).first()

        if audio_stream:
            audio_stream.stream_to_buffer(buffer)
            buffer.seek(0)

            # Set the appropriate headers for audio download
            headers = {
                "Content-Disposition": f'attachment; filename="{url.title}.mp3"',
                "Content-Type": "audio/mpeg"
            }

            return send_file(
                buffer,
                as_attachment=True,
                mimetype="audio/mpeg",
                download_name=f'{url.title}.mp3',
                headers=headers
            )
        else:
            return "No audio stream found for the provided YouTube link."

    return "Invalid or missing YouTube link parameter."

if __name__ == '__main__':
    app.run(debug=True)

