import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import YouTube
import tempfile
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        temp_filename = str(uuid.uuid4())
        video_file = tempfile.NamedTemporaryFile(delete=False, prefix=temp_filename)
        stream.download(output_path=video_file.name)
        return send_file(video_file.name, as_attachment=True, attachment_filename=f"{yt.title}.mp4")
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run()
