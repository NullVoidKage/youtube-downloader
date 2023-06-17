import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import YouTube
from io import BytesIO

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
        video_bytes = BytesIO()
        stream.download(output_path=video_bytes)
        video_bytes.seek(0)
        return send_file(video_bytes, attachment_filename=f"{yt.title}.mp4", as_attachment=True)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run()
