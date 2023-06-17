import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import YouTube
import tempfile
import uuid
import os

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
        temp_dir = tempfile.mkdtemp()
        temp_filename = str(uuid.uuid4())
        temp_filepath = os.path.join(temp_dir, temp_filename)
        stream.download(output_path=temp_filepath)
        return send_file(temp_filepath, as_attachment=True, attachment_filename=f"{yt.title}.mp4")
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run()
